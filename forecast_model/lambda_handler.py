import json
import boto3
import numpy as np
import pandas as pd
import warnings
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from insert_forecast_data import insert_forecast_data

# Forecasting imports
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

# Suppress warnings
warnings.filterwarnings("ignore")

# Configuration
SEASONAL_PERIOD = 12
TEST_HORIZON = 12
FORECAST_HORIZON = 6
LAGS = [1, 2, 3, 6, 12]
LOG_TRANSFORM = True  # for SARIMA only

def lambda_handler(event, context):
    """
    AWS Lambda handler for price forecasting
    
    Expected event structure:
    {
        "material_id": "string",
        "location_id": "string" (optional),
        "model_name": "string" (optional, defaults to 'Best')
    }
    
    Available model names:
    - "SARIMA"
    - "Linear Regression" 
    - "Random Forest"
    - "XGBoost"
    - "N-BEATS"
    - 'Best' (or omit model_name) - returns model with lowest MAPE
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "material_id": "string",
            "forecast_values": [float],
            "forecast_dates": [string],
            "model_used": "string",
            "mape": float,
            "model_details": "string"
        }
    }
    """
    try:
        # Parse input parameters
        material_id = event.get('material_id')
        location_id = event.get('location_id')
        model_name = event.get('model_name', 'Best')
        
        if not material_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'material_id is required'})
            }
        
        # Validate model name
        valid_models = ['SARIMA', 'Linear Regression', 'Random Forest', 'XGBoost', 'N-BEATS', 'Best']
        if model_name not in valid_models:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Invalid model_name. Must be one of: {valid_models}',
                    'available_models': valid_models
                })
            }
        
        # Fetch price history data
        price_data = fetch_price_history(material_id, location_id)

        print(f"price_data: {price_data.tail()}")
        
        if price_data.empty:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No price history data found for the given material_id'})
            }
        
        # Prepare time series
        series = prepare_time_series(price_data)
        
        if len(series) < 24:  # Minimum data requirement
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Insufficient historical data (minimum 24 months required)'})
            }
        
        # Run forecasting based on model_name
        if model_name == 'Best' or model_name is None:
            # Try all models and return the one with best MAPE
            results = run_all_models(series)
            if not results:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'All models failed to run'})
                }
            best_result = min(results, key=lambda x: x['mape'])
            # Use "Best(ActualModelName)" as model name for database storage when no specific model requested
            actual_model_name = best_result['model_name']
            best_result['model_name'] = f'Best({actual_model_name})'
        else:
            # Run specific model
            try:
                best_result = run_single_model(series, model_name)
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': f'Model {model_name} failed: {str(e)}'})
                }
        
        # Generate forecast dates - start from next month after last data point
        last_date = series.index[-1]
        # Get the next month after the last data point
        next_month = last_date + pd.DateOffset(months=1)
        forecast_dates = pd.date_range(
            start=next_month,
            periods=FORECAST_HORIZON,
            freq='MS'
        ).strftime('%Y-%m-%d').tolist()
        
        # Insert/Update forecast data in database
        try:
            print(f"best_result: {best_result}")
            insert_result = insert_forecast_data(
                material_id=material_id,
                location_id=location_id,
                model_name=best_result['model_name'],
                forecast_values=best_result['forecast'].tolist(),
                forecast_dates=forecast_dates,
                mape=best_result['mape'],
                model_details=best_result['details']
            )
            print(f"Database insert result: {insert_result}")
        except Exception as e:
            print(f"Failed to insert forecast data: {e}")
            # Continue with response even if database insert fails
        
        # Prepare response
        response_data = {
            'material_id': material_id,
            'forecast_values': best_result['forecast'].tolist(),
            'forecast_dates': forecast_dates,
            'mape': round(best_result['mape'], 3),
            'model_details': best_result['details']
        }
        
        # Show actual model name in response, but store as "Best(ModelName)" in database
        if model_name == 'Best' or model_name is None:
            # Find the actual best model name from results
            actual_model_name = min(results, key=lambda x: x['mape'])['model_name']
            response_data['model_used'] = actual_model_name
            response_data['model_used_for_storage'] = f'Best({actual_model_name})'
        else:
            response_data['model_used'] = best_result['model_name']
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def fetch_price_history(material_id: str, location_id: Optional[str] = None) -> pd.DataFrame:
    """
    Fetch price history data from database using the existing db_query function
    """
    # Import the database query function
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Pdf_Processor'))
    from db_query import database_query
    
    # Build query based on parameters
    if location_id:
        query = """
        SELECT period_start_date, period_end_date, price, price_currency, country
        FROM price_history_data 
        WHERE material_id = %s AND location_id = %s
        ORDER BY period_start_date
        """
        params = [material_id, location_id]
    else:
        query = """
        SELECT period_start_date, period_end_date, price, price_currency, country
        FROM price_history_data 
        WHERE material_id = %s
        ORDER BY period_start_date
        """
        params = [material_id]
    
    try:
        # Execute query
        result = database_query(query, params)
        
        # print(f"result: {result}")
        
        # Check if we got a successful response
        if not result or result.get('statusCode') != 200:
            print("Database query failed, using mock data")
            return create_mock_data(material_id, location_id)
        
        # Parse the JSON body
        try:
            records = json.loads(result['body'])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to parse database result: {e}, using mock data")
            return create_mock_data(material_id, location_id)
        
        if not records:
            print("No records found in database result, using mock data")
            return create_mock_data(material_id, location_id)
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        if df.empty:
            print("Empty DataFrame from database, using mock data")
            return create_mock_data(material_id, location_id)
        
        # print(f"df: {df.head()}")
        # Convert date columns
        df['period_start_date'] = pd.to_datetime(df['period_start_date'])
        df['period_end_date'] = pd.to_datetime(df['period_end_date'])
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        return df
        
    except Exception as e:
        print(f"Database query failed: {e}")
        # For testing purposes, return mock data
        return create_mock_data(material_id, location_id)


def create_mock_data(material_id: str, location_id: Optional[str] = None) -> pd.DataFrame:
    """
    Create mock price history data for testing when database is not available
    """
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Create 36 months of mock data
    start_date = datetime.now() - timedelta(days=36*30)
    dates = [start_date + timedelta(days=30*i) for i in range(36)]
    
    # Generate realistic price data with trend and seasonality
    base_price = 100.0
    prices = []
    for i, date in enumerate(dates):
        # Add trend (slight upward trend)
        trend = i * 0.5
        # Add seasonality (higher in winter months)
        seasonality = 10 * np.sin(2 * np.pi * date.month / 12)
        # Add some random noise
        noise = np.random.normal(0, 5)
        price = base_price + trend + seasonality + noise
        prices.append(max(price, 50))  # Ensure positive prices
    
    # Create DataFrame
    df = pd.DataFrame({
        'period_start_date': dates,
        'period_end_date': [d + timedelta(days=29) for d in dates],
        'price': prices,
        'price_currency': 'USD',
        'country': 'US'  # Default country
    })
    
    print(f"Created mock data for material {material_id}, location {location_id}: {len(df)} records")
    return df


def prepare_time_series(price_data: pd.DataFrame) -> pd.Series:
    """
    Prepare time series data from price history
    """
    # Group by month and take average price
    price_data['year_month'] = price_data['period_start_date'].dt.to_period('M')
    monthly_avg = price_data.groupby('year_month')['price'].mean()
    
    # Convert to datetime index
    monthly_avg.index = monthly_avg.index.to_timestamp()
    
    # Sort by date
    monthly_avg = monthly_avg.sort_index()
    
    # Remove any NaN values
    monthly_avg = monthly_avg.dropna()
    
    return monthly_avg


def safe_mape(y_true, y_pred):
    """Calculate MAPE safely handling division by zero"""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.size == 0:
        return np.nan
    eps = 1e-8
    return float(np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), eps))) * 100)


def seasonal_naive(series, horizon, m=12):
    """Seasonal naive forecast"""
    s = series.values
    if len(s) >= m:
        tmpl = s[-m:]
        return np.tile(tmpl, int(np.ceil(horizon/m)))[:horizon]
    return np.repeat(s[-1], horizon)


def is_explosive(fc_vals, history, window=24, factor=3.0):
    """Check if forecast values are explosive"""
    hist = history.dropna()
    if hist.empty:
        return False
    tail = hist.iloc[-min(window, len(hist)):]
    hi = np.nanmax(tail.values)
    fc_vals = np.asarray(fc_vals, dtype=float)
    if not np.all(np.isfinite(fc_vals)):
        return True
    return np.nanmax(fc_vals) > factor * hi


def sarimax_auto(series, seasonal_period=12):
    """Auto-select SARIMA parameters"""
    y = series.astype(float)
    pdq = [(p,d,q) for p in (0,1,2) for d in (0,1) for q in (0,1,2)]
    PDQ = [(P,D,Q,seasonal_period) for P in (0,1) for D in (0,1) for Q in (0,1)]
    best = {"aic": np.inf, "order": None, "sorder": None}
    
    for order in pdq:
        for sorder in PDQ:
            try:
                res = SARIMAX(
                    y, order=order, seasonal_order=sorder,
                    enforce_stationarity=True, enforce_invertibility=True
                ).fit(disp=False)
                if res.aic < best["aic"]:
                    best = {"aic": res.aic, "order": order, "sorder": sorder}
            except Exception:
                continue
    return best["order"], best["sorder"]


def make_features(series, lags=LAGS):
    """Create features for ML models"""
    df_feat = pd.DataFrame({"y": series})
    for lag in lags:
        df_feat[f"lag_{lag}"] = series.shift(lag)
    df_feat["month"] = series.index.month
    df_feat["year"] = series.index.year
    return df_feat.dropna()


def run_sarima(series):
    """Run SARIMA model"""
    if len(series) < (SEASONAL_PERIOD + TEST_HORIZON + 3):
        raise ValueError("Insufficient history for SARIMA.")
    
    train = series.iloc[:-TEST_HORIZON]
    test = series.iloc[-TEST_HORIZON:]
    train_fit = np.log1p(train) if LOG_TRANSFORM else train
    full_fit = np.log1p(series) if LOG_TRANSFORM else series

    order, sorder = sarimax_auto(train_fit, seasonal_period=SEASONAL_PERIOD)
    if order is None:
        raise RuntimeError("No SARIMA orders found.")
    
    # Fit model for evaluation
    m1 = SARIMAX(train_fit, order=order, seasonal_order=sorder,
                 enforce_stationarity=True, enforce_invertibility=True).fit(disp=False)
    test_fc_fit = m1.get_forecast(steps=TEST_HORIZON).predicted_mean.values
    test_fc = np.expm1(test_fc_fit) if LOG_TRANSFORM else test_fc_fit
    
    if is_explosive(test_fc, train):
        test_fc = seasonal_naive(train, TEST_HORIZON, m=SEASONAL_PERIOD)
    
    mape_val = safe_mape(test.values, test_fc)

    # Fit model for forecasting
    m2 = SARIMAX(full_fit, order=order, seasonal_order=sorder,
                 enforce_stationarity=True, enforce_invertibility=True).fit(disp=False)
    fut_fc_fit = m2.get_forecast(steps=FORECAST_HORIZON).predicted_mean.values
    fut_fc = np.expm1(fut_fc_fit) if LOG_TRANSFORM else fut_fc_fit
    
    if is_explosive(fut_fc, series):
        fut_fc = seasonal_naive(series, FORECAST_HORIZON, m=SEASONAL_PERIOD)

    details = f"SARIMA order={order}, seasonal_order={sorder}"
    
    return {
        'forecast': fut_fc,
        'mape': mape_val,
        'model_name': 'SARIMA',
        'details': details
    }


def run_ml_model(series, model_name):
    """Run ML model (Linear Regression, Random Forest, or XGBoost)"""
    min_needed = max(LAGS) + TEST_HORIZON + 6
    if len(series) < min_needed:
        raise ValueError("Insufficient history for ML model.")
    
    feat = make_features(series, lags=LAGS)
    X, y = feat.drop(columns=["y"]), feat["y"]
    X.index = y.index = feat.index
    train_idx = y.index[:-TEST_HORIZON]
    test_idx = y.index[-TEST_HORIZON:]
    X_train, y_train = X.loc[train_idx], y.loc[train_idx]
    X_test, y_test = X.loc[test_idx], y.loc[test_idx]

    # Get model
    if model_name == "Linear Regression":
        model = LinearRegression()
    elif model_name == "Random Forest":
        model = RandomForestRegressor(n_estimators=400, random_state=42, n_jobs=-1)
    elif model_name == "XGBoost":
        model = xgb.XGBRegressor(
            n_estimators=600, learning_rate=0.05, max_depth=4,
            subsample=0.9, colsample_bytree=0.9,
            objective="reg:squarederror", random_state=42, n_jobs=-1
        )
    else:
        raise ValueError(f"Unknown model: {model_name}")
    
    model.fit(X_train, y_train)
    test_fc = model.predict(X_test)
    mape_val = safe_mape(y_test.values, test_fc)

    # Recursive future forecasting
    future_vals = []
    last_known = series.copy()
    for step in range(FORECAST_HORIZON):
        next_date = last_known.index[-1] + pd.DateOffset(months=1)
        feat_row = {f"lag_{lag}": last_known.iloc[-lag] for lag in LAGS}
        feat_row["month"] = next_date.month
        feat_row["year"] = next_date.year
        X_future = pd.DataFrame([feat_row], index=[next_date])
        y_pred = float(model.predict(X_future)[0])
        future_vals.append(y_pred)
        last_known.loc[next_date] = y_pred
    
    fut_fc = np.array(future_vals)
    details = f"{model_name} with lags {LAGS} + month/year features"
    
    return {
        'forecast': fut_fc,
        'mape': mape_val,
        'model_name': model_name,
        'details': details
    }


def run_single_model(series, model_name):
    """Run a single specified model"""
    if model_name == "SARIMA":
        return run_sarima(series)
    elif model_name == "N-BEATS":
        return run_nbeats(series)
    else:
        return run_ml_model(series, model_name)


def run_nbeats(series):
    """Run N-BEATS model"""
    try:
        from darts import TimeSeries
        from darts.metrics import mape as darts_mape
        from darts.models import NBEATSModel
    except ImportError:
        raise RuntimeError("N-BEATS model requires darts library. Install with: pip install darts")
    
    if len(series) < 12 + TEST_HORIZON + 6:
        raise ValueError("Insufficient history for N-BEATS.")
    
    ts_all = TimeSeries.from_series(series)
    train_ts, test_ts = ts_all[:-TEST_HORIZON], ts_all[-TEST_HORIZON:]
    in_len_eval = max(6, min(18, len(train_ts) - TEST_HORIZON if len(train_ts) > TEST_HORIZON else 12))
    in_len_full = max(6, min(18, len(ts_all) - TEST_HORIZON if len(ts_all) > TEST_HORIZON else 12))

    model_eval = NBEATSModel(
        input_chunk_length=in_len_eval, output_chunk_length=TEST_HORIZON,
        n_epochs=100, batch_size=32, optimizer_kwargs={"lr":1e-3}, random_state=42)
    model_eval.fit(train_ts)
    pred_eval = model_eval.predict(TEST_HORIZON)

    model_full = NBEATSModel(
        input_chunk_length=in_len_full, output_chunk_length=FORECAST_HORIZON,
        n_epochs=100, batch_size=32, optimizer_kwargs={"lr":1e-3}, random_state=42)
    model_full.fit(ts_all)
    pred_future = model_full.predict(FORECAST_HORIZON)

    test_pd = pd.Series(test_ts.values().flatten(), index=test_ts.time_index)
    test_fc = pred_eval.values().flatten()
    fut_fc = pred_future.values().flatten()
    mape_val = float(darts_mape(test_ts, pred_eval))

    details = "N-BEATS neural network"
    
    return {
        'forecast': fut_fc,
        'mape': mape_val,
        'model_name': 'N-BEATS',
        'details': details
    }


def run_all_models(series):
    """Run all models and return results"""
    results = []
    model_names = ["SARIMA", "Linear Regression", "Random Forest", "XGBoost", "N-BEATS"]
    
    for model_name in model_names:
        try:
            if model_name == "SARIMA":
                result = run_sarima(series)
            elif model_name == "N-BEATS":
                result = run_nbeats(series)
            else:
                result = run_ml_model(series, model_name)
            results.append(result)
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue
    
    return results



if __name__ == "__main__":
    event = {
        "material_id": "100724-000000",
        "location_id": "212",
        "model_name": "Best"
    }
    lambda_handler(event, {})   