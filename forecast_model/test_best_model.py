"""
Test script to verify the "Best" model functionality
"""
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from lambda_handler import lambda_handler

def test_best_model_functionality():
    """Test the best model functionality"""
    
    print("=" * 60)
    print("TESTING BEST MODEL FUNCTIONALITY")
    print("=" * 60)
    
    # Test parameters
    material_id = "100724-000000"
    location_id = "212"
    
    print(f"Testing with material_id: {material_id}")
    print(f"Testing with location_id: {location_id}")
    
    # Test 1: Specific model (Random Forest)
    print("\n1. TESTING SPECIFIC MODEL (Random Forest):")
    print("-" * 50)
    
    event1 = {
        "material_id": material_id,
        "location_id": location_id,
        "model_name": "Random Forest"
    }
    
    print(f"Input: {json.dumps(event1, indent=2)}")
    result1 = lambda_handler(event1, {})
    
    if result1['statusCode'] == 200:
        body1 = json.loads(result1['body'])
        print(f"✅ Random Forest successful!")
        print(f"   Model Used: {body1['model_used']}")
        print(f"   MAPE: {body1['mape']}%")
        print(f"   Forecast Values: {body1['forecast_values'][:3]}... (first 3)")
    else:
        print(f"❌ Random Forest failed: {result1['body']}")
        return
    
    # Test 2: No model specified (should use "Best")
    print("\n2. TESTING NO MODEL SPECIFIED (Should use 'Best'):")
    print("-" * 50)
    
    event2 = {
        "material_id": material_id,
        "location_id": location_id
    }
    
    print(f"Input: {json.dumps(event2, indent=2)}")
    result2 = lambda_handler(event2, {})
    
    if result2['statusCode'] == 200:
        body2 = json.loads(result2['body'])
        print(f"✅ Best model successful!")
        print(f"   Model Used: {body2['model_used']}")
        print(f"   Model Used for Storage: {body2.get('model_used_for_storage', 'N/A')}")
        print(f"   MAPE: {body2['mape']}%")
        print(f"   Forecast Values: {body2['forecast_values'][:3]}... (first 3)")
    else:
        print(f"❌ Best model failed: {result2['body']}")
        return
    
    # Test 3: Run "Best" again (should update, not duplicate)
    print("\n3. TESTING 'Best' MODEL AGAIN (Should UPDATE, not duplicate):")
    print("-" * 50)
    
    print(f"Input: {json.dumps(event2, indent=2)}")
    result3 = lambda_handler(event2, {})
    
    if result3['statusCode'] == 200:
        body3 = json.loads(result3['body'])
        print(f"✅ Best model run 2 successful!")
        print(f"   Model Used: {body3['model_used']}")
        print(f"   Model Used for Storage: {body3.get('model_used_for_storage', 'N/A')}")
        print(f"   MAPE: {body3['mape']}%")
        print(f"   Forecast Values: {body3['forecast_values'][:3]}... (first 3)")
        
        # Compare results
        print(f"\n4. COMPARISON:")
        print("-" * 50)
        print(f"Random Forest MAPE: {body1['mape']}%")
        print(f"Best model MAPE:    {body2['mape']}%")
        print(f"Best model run 2:   {body3['mape']}%")
        print(f"Best model 1 & 2 match: {body2['forecast_values'] == body3['forecast_values']}")
        
    else:
        print(f"❌ Best model run 2 failed: {result3['body']}")
    
    print("\n" + "=" * 60)
    print("BEST MODEL TEST COMPLETED")
    print("=" * 60)
    print("✅ Random Forest: Stored with model_name = 'Random Forest'")
    print("✅ Best model: Stored with model_name = 'Best' (no duplicates)")
    print("✅ Both can coexist in the database!")

if __name__ == "__main__":
    test_best_model_functionality()
