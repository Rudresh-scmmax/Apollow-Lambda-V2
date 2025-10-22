# Forecast Recommendation Function

This module provides AI-powered procurement recommendations based on forecasted price data using AWS Bedrock's Llama model.

## Features

- Fetches forecast price data from the database
- Analyzes price trends, volatility, and patterns
- Generates procurement strategies using AI
- Saves recommendations to the database
- Returns structured recommendation data

## API Usage

### Request Format

```json
{
    "action": "forecast_recommendation",
    "material_id": "M036",
    "location_id": 1
}
```

### Response Format

```json
{
    "statusCode": 200,
    "body": {
        "message": "Forecast recommendation generated and saved successfully",
        "data": {
            "material": "Material_M036",
            "generated_at": "2024-01-15 10:30:00",
            "recommendation": "Based on the forecast, consider...",
            "strategies": {
                "conservative": "Risk-averse strategy...",
                "balanced": "Moderate risk strategy...",
                "aggressive": "Risk-tolerant strategy..."
            }
        }
    }
}
```

## Database Schema

### forecast_recommendations Table

```sql
CREATE TABLE forecast_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id VARCHAR(50) NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    material_name VARCHAR(255) NOT NULL,
    recommendation TEXT NOT NULL,
    conservative_strategy TEXT NOT NULL,
    balanced_strategy TEXT NOT NULL,
    aggressive_strategy TEXT NOT NULL,
    generated_at DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_material_location (material_id, location_id),
    INDEX idx_generated_at (generated_at),
    INDEX idx_created_at (created_at)
);
```

## Dependencies

- `boto3` - AWS SDK for Bedrock integration
- `pandas` - Data manipulation
- `numpy` - Numerical operations

## AWS Requirements

- AWS Bedrock access with Llama 4 Scout model permissions
- Proper IAM roles for Bedrock runtime access

## Files

- `forecast_recommendation.py` - Main recommendation logic
- `lambda_handler.py` - Updated with forecast recommendation action
- `create_forecast_recommendations_table.sql` - Database schema
- `test_forecast_recommendation.py` - Test script
- `requirements.txt` - Updated dependencies

## Error Handling

The function handles various error scenarios:
- Missing parameters
- Database connection issues
- AI model failures
- Data format issues

All errors are logged and returned with appropriate HTTP status codes.
