"""
Test script for forecast recommendation functionality using AWS Bedrock
"""
import json

# Example test event for the forecast recommendation
test_event = {
    "action": "forecast_recommendation",
    "material_id": "100724-000000",
    "location_id": "212"
}

# Example of how to call the lambda function
def test_forecast_recommendation():
    """
    Test function to demonstrate how to use the forecast recommendation with Bedrock
    """
    from lambda_handler import lambda_handler
    
    # Mock context (not used in this implementation)
    class MockContext:
        def __init__(self):
            self.function_name = "test_function"
            self.function_version = "1"
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test_function"
            self.memory_limit_in_mb = 128
            self.remaining_time_in_millis = 30000
    
    context = MockContext()
    
    try:
        result = lambda_handler(test_event, context)
        print("Test Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        return None

def test_bedrock_integration():
    """
    Test the Bedrock integration directly
    """
    from forecast_recommendation import generate_procurement_strategy_bedrock
    
    # Sample forecast data
    sample_forecast = [615.0, 618.5, 620.0, 617.8, 616.2, 614.0, 610.0, 608.0, 607.0, 609.0,
                      612.5, 615.0, 617.0, 618.0, 620.5, 621.0, 622.0, 623.0, 624.5, 625.0,
                      624.0, 622.5, 621.0, 619.0]
    
    try:
        result = generate_procurement_strategy_bedrock(
            forecast_price=sample_forecast,
            material="Test Material",
            verbose=False
        )
        print("Bedrock Integration Test Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"Bedrock test failed with error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Testing Forecast Recommendation Function with AWS Bedrock")
    print("=" * 60)
    
    print("\n1. Testing Bedrock Integration:")
    test_bedrock_integration()
    
    print("\n2. Testing Full Lambda Handler:")
    test_forecast_recommendation()
