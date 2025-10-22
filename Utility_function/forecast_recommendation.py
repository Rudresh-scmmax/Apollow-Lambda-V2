import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
import re
import boto3
from db_query import database_query

# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ARNs
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"


def invoke_bedrock_text(system_msg, user_content, temperature=0.1, max_tokens=4096):
    """
    Invoke Bedrock's Llama 4 Scout text model using Converse API.
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {"text": user_content.strip()}
                ]
            }
        ]
        
        response = bedrock.converse(
            modelId=TEXT_MODEL_ARN,
            messages=messages,
            system=[{"text": system_msg.strip()}],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9
            }
        )
        
        # Extract text from response
        text = ""
        if response.get('output') and response['output'].get('message'):
            content = response['output']['message'].get('content', [])
            if content and len(content) > 0:
                text = content[0].get('text', '')
        
        # Clean up markdown if present
        text = text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text)
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {text}")
        return None
    except Exception as e:
        print(f"Bedrock invocation failed: {e}")
        return None


def generate_procurement_strategy_bedrock(forecast_price, material, verbose=False):
    """
    Analyze forecasted prices and generate a procurement recommendation
    using AWS Bedrock's Llama model. Time frame is derived from the length of forecast_df.

    If verbose is False, LLM gives only the final strategies with no reasoning.
    """

    time_frame = len(forecast_price)

    # Fetch key price features from the forecast
    first = forecast_price[0]
    last = forecast_price[-1]
    peak = max(forecast_price)
    low = min(forecast_price)
    volatility = np.std(forecast_price)
    peak_month = forecast_price.index(peak) + 1
    trend = "rising" if last > first else "falling" if last < first else "flat"

    prices_str = "\n".join([f"Month {i+1}: {p:.2f}" for i, p in enumerate(forecast_price)])

    system_msg = """You are an expert procurement strategy analyst. Analyze forecasted price data and provide procurement recommendations with three risk-based strategies."""

    user_content = f"""
    Analyze the following forecast data for {material} and provide procurement recommendations.

    Material: {material}
    Forecast Time Frame: {time_frame} months

    Forecasted Prices:
    {prices_str}

    Summary:
    Start Price: {first:.2f}
    Peak Price: {peak:.2f} in Month {peak_month}
    End Price: {last:.2f}
    Trend: {trend}
    Volatility (standard deviation): {volatility:.2f}

    Based on this forecast data, provide a procurement recommendation and three strategies.

    Return your analysis in this exact JSON format:
    {{
        "material": "{material}",
        "generated_at": "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "recommendation": "Your overall procurement recommendation based on the forecast analysis",
        "strategies": {{
            "conservative": "Risk-averse procurement strategy for {material}",
            "balanced": "Moderate risk procurement strategy for {material}",
            "aggressive": "Risk-tolerant procurement strategy for {material}"
        }}
    }}

    Only return valid JSON. No markdown formatting.
    """

    result = invoke_bedrock_text(system_msg, user_content)
    
    if result is not None:
        return result
    else:
        # Fallback if analysis fails
        return {
            "material": material,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendation": "Analysis generation failed - unable to provide recommendation",
            "strategies": {
                "conservative": "Unable to generate conservative strategy",
                "balanced": "Unable to generate balanced strategy", 
                "aggressive": "Unable to generate aggressive strategy"
            }
        }


def get_forecast_price_data(material_id, location_id):
    """
    Fetch forecast price data from the database for the given material_id and location_id.
    """
    query = """
    SELECT forecast_date, forecast_value 
    FROM price_forecast_data 
    WHERE material_id = %s AND location_id = %s 
    ORDER BY forecast_date ASC
    """
    
    result = database_query(query, [material_id, location_id])
    
    if result.get('statusCode') == 200:
        data = result.get('body', [])
        
        # Handle case where body is a string (JSON)
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = []
        
        if data and len(data) > 0:
            # Extract forecast prices from the data
            forecast_prices = [float(row['forecast_value']) for row in data]
            return forecast_prices
        else:
            raise Exception(f"No forecast data found for material_id: {material_id} and location_id: {location_id}")
    else:
        error_msg = result.get('error', 'Unknown error')
        raise Exception(f"Database query failed: {error_msg}")


def insert_forecast_recommendation(material_id, location_id, recommendation_data):
    """
    Insert forecast recommendation data into the forecast_recommendations table.
    """
    query = """
    INSERT INTO forecast_recommendations 
    (material_id, location_id, material_name, recommendation, conservative_strategy, 
     balanced_strategy, aggressive_strategy, generated_at, created_at) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    params = [
        material_id,
        location_id,
        recommendation_data['material'],
        recommendation_data['recommendation'],
        recommendation_data['strategies']['conservative'],
        recommendation_data['strategies']['balanced'],
        recommendation_data['strategies']['aggressive'],
        recommendation_data['generated_at'],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    
    result = database_query(query, params)
    return result


def lambda_handler(event, context):
    """
    AWS Lambda handler for forecast recommendation generation.
    
    Expected event structure:
    {
        "material_id": "M036",
        "location_id": 1
    }
    """
    try:
        material_id = event.get("material_id")
        location_id = event.get("location_id")
        
        if not material_id or not location_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing 'material_id' or 'location_id' parameter"
                })
            }
        
        # Get forecast price data
        forecast_prices = get_forecast_price_data(material_id, location_id)
        
        # Generate material name (you might want to fetch this from database)
        material_name = f"Material_{material_id}"
        
        # Generate procurement strategy using Bedrock
        recommendation_data = generate_procurement_strategy_bedrock(
            forecast_price=forecast_prices,
            material=material_name,
            verbose=False
        )
        
        # Insert recommendation into database
        insert_result = insert_forecast_recommendation(material_id, location_id, recommendation_data)
        
        if insert_result.get('statusCode') == 200:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Forecast recommendation generated and saved successfully",
                    "data": recommendation_data
                })
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Failed to save recommendation to database",
                    "details": insert_result
                })
            }
            
    except Exception as e:
        print(f"Error generating forecast recommendation: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Error generating forecast recommendation: {str(e)}"
            })
        }


if __name__ == "__main__":
    test_event = {
        "material_id": "100724-000000",
        "location_id": "212"
    }
    result = lambda_handler(test_event, None)
    print(result)