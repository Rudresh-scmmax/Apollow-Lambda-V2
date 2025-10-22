"""
Debug script to check the last historical date and forecast dates
"""
import json
import sys
import os
import pandas as pd

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from lambda_handler import lambda_handler

def debug_dates():
    """Debug the date logic"""
    
    print("=" * 60)
    print("DEBUGGING DATE LOGIC")
    print("=" * 60)
    
    # Test parameters
    material_id = "100724-000000"
    location_id = "212"
    
    print(f"Testing with material_id: {material_id}")
    print(f"Testing with location_id: {location_id}")
    
    # Test without model name to get best model
    event = {
        "material_id": material_id,
        "location_id": location_id
    }
    
    print(f"Input: {json.dumps(event, indent=2)}")
    result = lambda_handler(event, {})
    
    if result['statusCode'] == 200:
        body = json.loads(result['body'])
        print(f"✅ Success!")
        print(f"   Model Used: {body['model_used']}")
        print(f"   MAPE: {body['mape']}%")
        print(f"   Forecast Values: {body['forecast_values']}")
        print(f"   Forecast Dates: {body['forecast_dates']}")
        
        # Let's also check what the last historical date should be
        print(f"\n📅 Forecast should start from: {body['forecast_dates'][0]}")
        print(f"📅 This means last historical data was before: {body['forecast_dates'][0]}")
        
    else:
        print(f"❌ Failed: {result['body']}")

if __name__ == "__main__":
    debug_dates()
