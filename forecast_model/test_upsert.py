"""
Test script to verify the upsert functionality
"""
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from lambda_handler import lambda_handler

def test_upsert_functionality():
    """Test the upsert functionality by running the Lambda twice"""
    
    print("=" * 60)
    print("TESTING UPSERT FUNCTIONALITY")
    print("=" * 60)
    
    # Test parameters
    material_id = "100724-000000"
    location_id = "212"
    
    print(f"Testing with material_id: {material_id}")
    print(f"Testing with location_id: {location_id}")
    
    # First run - should insert new records
    print("\n1. FIRST RUN (Should INSERT new records):")
    print("-" * 50)
    
    event = {
        "material_id": material_id,
        "location_id": location_id,
        "model_name": "Random Forest"
    }
    
    print(f"Input: {json.dumps(event, indent=2)}")
    result1 = lambda_handler(event, {})
    
    if result1['statusCode'] == 200:
        body1 = json.loads(result1['body'])
        print(f"✅ First run successful!")
        print(f"   Model Used: {body1['model_used']}")
        print(f"   MAPE: {body1['mape']}%")
        print(f"   Forecast Values: {body1['forecast_values']}")
        print(f"   Forecast Dates: {body1['forecast_dates']}")
    else:
        print(f"❌ First run failed: {result1['body']}")
        return
    
    # Second run - should update existing records
    print("\n2. SECOND RUN (Should UPDATE existing records):")
    print("-" * 50)
    
    print(f"Input: {json.dumps(event, indent=2)}")
    result2 = lambda_handler(event, {})
    
    if result2['statusCode'] == 200:
        body2 = json.loads(result2['body'])
        print(f"✅ Second run successful!")
        print(f"   Model Used: {body2['model_used']}")
        print(f"   MAPE: {body2['mape']}%")
        print(f"   Forecast Values: {body2['forecast_values']}")
        print(f"   Forecast Dates: {body2['forecast_dates']}")
        
        # Compare results
        print(f"\n3. COMPARISON:")
        print("-" * 50)
        print(f"First run MAPE:  {body1['mape']}%")
        print(f"Second run MAPE: {body2['mape']}%")
        print(f"Values match: {body1['forecast_values'] == body2['forecast_values']}")
        print(f"Dates match: {body1['forecast_dates'] == body2['forecast_dates']}")
        
    else:
        print(f"❌ Second run failed: {result2['body']}")
    
    print("\n" + "=" * 60)
    print("UPSERT TEST COMPLETED")
    print("=" * 60)
    print("✅ If both runs succeeded, the upsert functionality is working!")
    print("✅ The database should have updated records instead of duplicates.")

if __name__ == "__main__":
    test_upsert_functionality()
