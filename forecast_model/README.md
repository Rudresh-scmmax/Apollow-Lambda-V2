# Price Forecasting Lambda Function

This Lambda function provides price forecasting capabilities using multiple machine learning models.

## Features

- **Multiple Models**: SARIMA, Linear Regression, Random Forest, and XGBoost
- **Automatic Model Selection**: Returns the model with the best MAPE (Mean Absolute Percentage Error)
- **Database Integration**: Fetches price history from the existing database
- **Flexible Input**: Supports material_id, optional location_id, and model selection

## Input Format

```json
{
    "material_id": "string (required)",
    "location_id": "string (optional)",
    "model_name": "string (optional, defaults to 'best')"
}
```

### Available Model Names:
- `"SARIMA"` - Seasonal AutoRegressive Integrated Moving Average
- `"Linear Regression"` - Linear regression with lag features
- `"Random Forest"` - Random Forest with 400 estimators
- `"XGBoost"` - XGBoost gradient boosting
- `"N-BEATS"` - Neural Basis Expansion Analysis for Time Series
- `"best"` or omit `model_name` - Automatically selects model with lowest MAPE

## Output Format

```json
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
```

## Available Models

- **SARIMA**: Seasonal AutoRegressive Integrated Moving Average
- **Linear Regression**: Simple linear regression with lag features
- **Random Forest**: Ensemble method with 400 estimators
- **XGBoost**: Gradient boosting with optimized parameters
- **N-BEATS**: Neural network for time series forecasting

## Configuration

- **Forecast Horizon**: 6 months
- **Test Horizon**: 12 months (for model evaluation)
- **Seasonal Period**: 12 months
- **Feature Lags**: [1, 2, 3, 6, 12] months

## Deployment

1. Package the function with dependencies
2. Deploy to AWS Lambda
3. Configure appropriate IAM permissions for database access
4. Set environment variables if needed

## Dependencies

- boto3: AWS SDK
- pandas: Data manipulation
- numpy: Numerical computing
- scikit-learn: Machine learning
- statsmodels: Statistical models
- xgboost: Gradient boosting
