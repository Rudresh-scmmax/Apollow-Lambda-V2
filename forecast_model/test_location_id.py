"""
Test script using location_id instead of region
Tests with location_id = 212
"""
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from lambda_handler import lambda_handler

def test_with_location_id():
    """Test the functionality with location_id"""
    
    print("=" * 60)
    print("TESTING WITH LOCATION_ID")
    print("=" * 60)
    
    # Test parameters
    material_id = "100724-000000"
    location_id = "212"
    
    print(f"Testing with material_id: {material_id}")
    print(f"Testing with location_id: {location_id}")
    
    # Test 1: No model specified (should return best model with least MAPE)
    print("\n1. Testing with NO model specified (should return best model):")
    print("-" * 50)
    
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
        print(f"   Model Details: {body['model_details']}")
    else:
        print(f"❌ Failed: {result['body']}")
    
    # Test 2: Specific model specified
    print("\n2. Testing with specific model (Random Forest):")
    print("-" * 50)
    
    event = {
        "material_id": material_id,
        "location_id": location_id,
        "model_name": "Random Forest"
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
        print(f"   Model Details: {body['model_details']}")
    else:
        print(f"❌ Failed: {result['body']}")
    
    # Test 3: Test all available models and compare MAPE
    print("\n3. Testing all available models and comparing MAPE:")
    print("-" * 50)
    
    models = ["SARIMA", "Linear Regression", "Random Forest", "XGBoost", "N-BEATS"]
    results = []
    
    for model in models:
        print(f"\nTesting {model}...")
        event = {
            "material_id": material_id,
            "location_id": location_id,
            "model_name": model
        }
        
        result = lambda_handler(event, {})
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            results.append((model, body['mape']))
            print(f"   ✅ {model}: MAPE = {body['mape']:.3f}%")
            print(f"      Forecast: {body['forecast_values'][:3]}... (first 3 values)")
        else:
            print(f"   ❌ {model}: Failed - {result['body']}")
    
    # Find best model
    if results:
        best_model, best_mape = min(results, key=lambda x: x[1])
        print(f"\n🏆 Best model: {best_model} with MAPE: {best_mape:.3f}%")
        
        # Show all results sorted by MAPE
        print(f"\nAll models sorted by MAPE (best to worst):")
        sorted_results = sorted(results, key=lambda x: x[1])
        for i, (model, mape) in enumerate(sorted_results, 1):
            print(f"   {i}. {model}: {mape:.3f}%")
    
    # Test 4: Without location_id (should still work)
    print("\n4. Testing WITHOUT location_id:")
    print("-" * 50)
    
    event = {
        "material_id": material_id
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
    else:
        print(f"❌ Failed: {result['body']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_with_location_id()
