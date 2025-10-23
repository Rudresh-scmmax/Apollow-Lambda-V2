"""
Simple test to verify the demand_supply_summary integration works.
This tests the new methods added to existing files.
"""

from extract_market_intelligence import DatabaseManager
from llm_module import summarize_demand_supply_with_bedrock


def test_summarization_function():
    """Test the summarization function from llm_module."""
    print("Testing summarization function...")
    
    # Sample data
    demand_data = [
        {'demand_impact': 'Strong demand from pharmaceutical sector'},
        {'demand_impact': 'Increased demand from personal care industry'}
    ]
    
    supply_data = [
        {'supply_impact': 'Supply constraints due to plant maintenance'},
        {'supply_impact': 'Logistical delays affecting supply chain'}
    ]
    
    try:
        result = summarize_demand_supply_with_bedrock(
            demand_data, supply_data, "M001", 1, "2024-01-15"
        )
        print(f"Summarization result: {result}")
        return True
    except Exception as e:
        print(f"Summarization test failed: {e}")
        return False


def test_database_manager_methods():
    """Test the new methods added to DatabaseManager."""
    print("Testing DatabaseManager methods...")
    
    try:
        db = DatabaseManager()
        
        # Test get_demand_supply_data method
        print("Testing get_demand_supply_data...")
        data = db.get_demand_supply_data("M001", 1, "2024-01-15")
        print(f"Retrieved data: {data}")
        
        # Test process_demand_supply_summary method
        print("Testing process_demand_supply_summary...")
        result = db.process_demand_supply_summary("M001", 1, "2024-01-15")
        print(f"Process result: {result}")
        
        return True
    except Exception as e:
        print(f"DatabaseManager test failed: {e}")
        return False


def main():
    """Run integration tests."""
    print("=== Demand Supply Summary Integration Test ===")
    
    # Test 1: Summarization function
    test1_passed = test_summarization_function()
    
    # Test 2: DatabaseManager methods
    test2_passed = test_database_manager_methods()
    
    print(f"\n=== Test Results ===")
    print(f"Summarization function: {'PASS' if test1_passed else 'FAIL'}")
    print(f"DatabaseManager methods: {'PASS' if test2_passed else 'FAIL'}")
    
    if test1_passed and test2_passed:
        print("✅ All integration tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")


if __name__ == "__main__":
    main()
