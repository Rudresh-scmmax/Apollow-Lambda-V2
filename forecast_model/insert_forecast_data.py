"""
Function to insert forecast data into the price_forecast_data table
Use this in your Lambda function after generating forecasts
"""
import json
from datetime import datetime, date
from typing import List, Dict, Optional

def insert_forecast_data(material_id: str, location_id: Optional[str], 
                        model_name: str, forecast_values: List[float], 
                        forecast_dates: List[str], mape: float, 
                        model_details: str) -> Dict:
    """
    Insert forecast data into the database
    
    Args:
        material_id: Material ID
        location_id: Location ID (can be None)
        model_name: Name of the model used
        forecast_values: List of forecast values
        forecast_dates: List of forecast dates (ISO format strings)
        mape: Mean Absolute Percentage Error
        model_details: Model configuration details
    
    Returns:
        Dict with success status and inserted record count
    """
    try:
        # Import the database query function
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Pdf_Processor'))
        from db_query import database_query
        
        # Prepare the upsert query (INSERT ... ON CONFLICT DO UPDATE)
        upsert_query = """
        INSERT INTO price_forecast_data (
            material_id, 
            location_id, 
            model_name, 
            forecast_date, 
            forecast_value, 
            mape, 
            model_details,
            created_at,
            created_by
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, 'forecast_lambda')
        ON CONFLICT (material_id, location_id, model_name, forecast_date) 
        DO UPDATE SET
            forecast_value = EXCLUDED.forecast_value,
            mape = EXCLUDED.mape,
            model_details = EXCLUDED.model_details,
            created_at = CURRENT_TIMESTAMP,
            created_by = 'forecast_lambda'
        """
        
        inserted_count = 0
        
        # Insert each forecast value
        for i, (forecast_date, forecast_value) in enumerate(zip(forecast_dates, forecast_values)):
            params = [
                material_id,
                location_id,
                model_name,
                forecast_date,
                float(forecast_value),
                float(mape),
                model_details
            ]
            
            result = database_query(upsert_query, params)
            
            if result.get('statusCode') == 200:
                inserted_count += 1
            else:
                print(f"Failed to insert forecast for date {forecast_date}: {result}")
        
        return {
            'success': True,
            'upserted_count': inserted_count,
            'total_forecasts': len(forecast_values),
            'message': f'Successfully upserted {inserted_count} forecast records'
        }
        
    except Exception as e:
        print(f"Error inserting forecast data: {e}")
        return {
            'success': False,
            'error': str(e),
            'inserted_count': 0
        }

def get_latest_forecasts(material_id: str, location_id: Optional[str] = None) -> List[Dict]:
    """
    Retrieve latest forecasts for a material
    
    Args:
        material_id: Material ID
        location_id: Location ID (optional)
    
    Returns:
        List of forecast records
    """
    try:
        # Import the database query function
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Pdf_Processor'))
        from db_query import database_query
        
        query = """
        SELECT 
            forecast_date,
            forecast_value,
            model_name,
            mape,
            model_details,
            created_at
        FROM price_forecast_data 
        WHERE material_id = %s 
            AND (location_id = %s OR location_id IS NULL)
        ORDER BY forecast_date ASC, created_at DESC
        """
        
        params = [material_id, location_id]
        result = database_query(query, params)
        
        if result.get('statusCode') == 200:
            return json.loads(result['body'])
        else:
            return []
            
    except Exception as e:
        print(f"Error retrieving forecasts: {e}")
        return []

# Example usage in Lambda function:
"""
# After generating forecasts in your Lambda function:

# Insert the forecast data
insert_result = insert_forecast_data(
    material_id=material_id,
    location_id=location_id,
    model_name=best_result['model_name'],
    forecast_values=best_result['forecast'],
    forecast_dates=forecast_dates,
    mape=best_result['mape'],
    model_details=best_result['details']
)

print(f"Inserted {insert_result['inserted_count']} forecast records")
"""
