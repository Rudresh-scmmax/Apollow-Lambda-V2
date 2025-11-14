import math
import re
import pandas as pd
import json
import boto3
from datetime import datetime
from typing import Dict, List, Optional, Any
from db_query import database_query

# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"


def _parse_db_result(result):
    """Helper to parse database_query results"""
    # Check for errors first
    if isinstance(result, dict) and result.get('statusCode') == 500:
        print(f"Database query error: {result.get('error')}")
        return []
    
    # Handle different response formats
    if isinstance(result, str):
        try:
            body = json.loads(result)
        except json.JSONDecodeError:
            print(f"Failed to parse string result: {result}")
            return []
    elif isinstance(result, dict) and "body" in result:
        try:
            body = json.loads(result["body"]) if isinstance(result["body"], str) else result["body"]
        except json.JSONDecodeError:
            print(f"Failed to parse body: {result['body']}")
            return []
    else:
        body = result
    
    if not isinstance(body, list):
        print(f"Expected list but got: {type(body)} - {body}")
        return []
    
    return body


def fetch_material_price_history(material_ids: List[str] = None):
    """Fetch price history data from price_history_data table."""
    try:
        if material_ids:
            # Query specific materials
            placeholders = ','.join(['%s'] * len(material_ids))
            query = f"""
                SELECT 
                    phd.material_id,
                    mm.material_description,
                    phd.period_start_date,
                    phd.period_end_date,
                    phd.price,
                    phd.price_currency,
                    phd.country,
                    phd.price_type
                FROM price_history_data phd
                JOIN material_master mm ON phd.material_id = mm.material_id
                WHERE phd.material_id IN ({placeholders})
                    AND phd.price IS NOT NULL
                ORDER BY phd.material_id, phd.period_start_date
            """
            print(f"[DEBUG] Querying for specific materials: {material_ids}")
            result = database_query(query, material_ids)
        else:
            # Query all materials
            query = """
                SELECT 
                    phd.material_id,
                    mm.material_description,
                    phd.period_start_date,
                    phd.period_end_date,
                    phd.price,
                    phd.price_currency,
                    phd.country,
                    phd.price_type
                FROM price_history_data phd
                JOIN material_master mm ON phd.material_id = mm.material_id
                WHERE phd.price IS NOT NULL
                ORDER BY phd.material_id, phd.period_start_date
            """
            print("[DEBUG] Querying for all materials (this may take a while for large datasets)")
            result = database_query(query)
        
        print(f"[DEBUG] Database query result type: {type(result)}")
        rows = _parse_db_result(result)
        print(f"[DEBUG] Parsed {len(rows)} rows from database")
        
        if not rows:
            print("[WARNING] No rows returned from database")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        print(f"[DEBUG] Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"Error fetching price history: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return pd.DataFrame()


def get_material_name(material_id: str) -> Optional[str]:
    """Get material description from material_master table."""
    try:
        query = "SELECT material_description FROM material_master WHERE material_id = %s LIMIT 1"
        result = database_query(query, [material_id])
        rows = _parse_db_result(result)
        if rows and len(rows) > 0:
            return rows[0].get("material_description")
        return None
    except Exception as e:
        print(f"Error fetching material name: {e}")
        return None


def process_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process price history data for correlation analysis."""
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Convert dates to datetime
    df['period_start_date'] = pd.to_datetime(df['period_start_date'], errors='coerce')
    df['period_end_date'] = pd.to_datetime(df['period_end_date'], errors='coerce')
    
    # Use period_start_date as the date for grouping
    df['date'] = df['period_start_date']
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Create year_month for grouping
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Remove rows with invalid dates or prices
    df = df.dropna(subset=['date', 'price', 'material_id', 'year_month'])
    
    return df


def calculate_correlations(df: pd.DataFrame, target_material_id: str) -> Dict[str, Any]:
    """Calculate correlation matrix and find most correlated material."""
    if df is None or df.empty:
        return None, None, {}
    
    # Group by year_month and material_id, calculate average price
    monthly_avg = (
        df.groupby(['year_month', 'material_id'])['price']
        .mean()
        .reset_index()
    )
    
    print(f"[DEBUG] Monthly average data shape: {monthly_avg.shape}")
    print(f"[DEBUG] Unique materials in monthly_avg: {list(monthly_avg['material_id'].unique())}")
    
    # Pivot to have materials as columns and year_month as index
    pivot_df = monthly_avg.pivot_table(
        index='year_month', 
        columns='material_id', 
        values='price'
    )
    
    print(f"[DEBUG] Pivot table shape: {pivot_df.shape}")
    print(f"[DEBUG] Pivot table columns (material_ids): {list(pivot_df.columns)}")
    
    # Forward fill and backward fill to handle missing values
    filled_df = pivot_df.ffill().bfill()
    
    # Calculate correlation matrix
    correlation_matrix = filled_df.corr()

    print(f"[DEBUG] Correlation matrix shape: {correlation_matrix.shape}")
    print(f"[DEBUG] Correlation matrix columns: {list(correlation_matrix.columns)}")
    print(f"[DEBUG] Target material_id type: {type(target_material_id)}, value: {target_material_id}")
    
    if target_material_id not in correlation_matrix.columns:
        print(f"[ERROR] Target material {target_material_id} not found in correlation matrix columns")
        print(f"[DEBUG] Available columns: {list(correlation_matrix.columns)}")
        return None, None, {}
    
    # Get correlations for target material
    material_correlations = correlation_matrix[target_material_id].drop(labels=[target_material_id])
    
    # Find most correlated material using absolute correlation (strongest correlation regardless of direction)
    # This handles both positive and negative correlations
    abs_correlations = material_correlations.abs()
    most_correlated_id = abs_correlations.idxmax()
    most_correlation_value = material_correlations[most_correlated_id]
    
    # Sort all correlations by absolute value (descending) for the output
    material_correlations_sorted = material_correlations.reindex(
        material_correlations.abs().sort_values(ascending=False).index
    )
    
    # Convert to dict, handling NaN values
    all_correlations = {
        k: (None if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v))
        for k, v in material_correlations_sorted.to_dict().items()
    }
    
    return most_correlated_id, most_correlation_value, all_correlations


def format_data_for_bedrock(df: pd.DataFrame, material_names: Dict[str, str]) -> str:
    """Format price data for Bedrock analysis."""
    if df is None or df.empty:
        return ""
    
    # Group by material and month
    monthly_avg = (
        df.groupby(['year_month', 'material_id'])['price']
        .mean()
        .reset_index()
    )
    
    full_prompt_text = ""
    for material_id in monthly_avg['material_id'].unique():
        material_df = monthly_avg[monthly_avg['material_id'] == material_id]
        material_df = material_df.sort_values('year_month')
        
        material_name = material_names.get(material_id, material_id)
        formatted_text = f"Material: {material_name}\n"
        formatted_text += "Month\tAvg Price\n"
        formatted_text += "----------------------\n"
        
        for _, row in material_df.iterrows():
            year_month_str = str(row['year_month'])
            price = row['price']
            formatted_text += f"{year_month_str}\t{price:.2f}\n"
        
        formatted_text += "\n"
        full_prompt_text += formatted_text
    
    return full_prompt_text


def invoke_bedrock_text(system_msg: str, user_content: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    """Invoke Bedrock text model and return response."""
    try:
        response = bedrock.converse(
            modelId=TEXT_MODEL_ARN,
            system=[{"text": system_msg.strip()}] if system_msg else [],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"text": user_content.strip()}
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9
            }
        )
        
        if response.get("output") and response["output"].get("message"):
            content = response["output"]["message"].get("content", [])
            if content:
                return content[0].get("text", "").strip()
        return ""
    except Exception as e:
        print(f"Bedrock invocation failed: {e}")
        return ""


def generate_key_takeaways(data_text: str, material_names: Dict[str, str], target_material_id: str, 
                          most_correlated_id: str, correlation_value: float) -> str:
    """Generate key takeaways using Bedrock."""
    try:
        name_list = [material_names.get(code, code) for code in material_names.keys()]
        target_name = material_names.get(target_material_id, target_material_id)
        correlated_name = material_names.get(most_correlated_id, most_correlated_id) if most_correlated_id else "N/A"
        
        system_msg = (
            "You are an expert in procurement analytics and market trend analysis. "
            "Analyze price data and provide concise summaries in plain text format only. "
            "Do not use markdown formatting, asterisks, or hash symbols."
        )
        
        prompt = f"""
You are an expert in procurement analytics and market trend analysis. Below is average monthly price data for materials: {', '.join(name_list)}.

Your task:
1. Analyze the data to detect:
   - Seasonal or multi-year cycles
   - Long-term trends (upward, downward, stable)
   - Significant price anomalies or outliers
   - Correlation behavior between the materials (are their cycles aligned or different?)

2. Write a summary suitable for a procurement dashboard.

Guidelines:
- Write 1 to 3 short sentences per material.
- Be precise and factual.
- Mention the presence or absence of cycles.
- Comment on current position in the cycle (e.g. nearing peak, bottoming out).
- Highlight any major trends or anomalies.
- Use business-friendly language suitable for procurement and finance users.
- IMPORTANT: Use ONLY material names (e.g., "Glycerine", "Phenol") in your response. Do NOT include material IDs or codes.
- CRITICAL: Do NOT use markdown formatting. No asterisks (**), no hash symbols (##), no bold text. Use plain text only.
- Format each material on a new line starting with the material name followed by a colon.
- Include a "General Insights:" section at the end if there are cross-material observations.

Context:
- Target material: {target_name}
- Most correlated material: {correlated_name}
- Correlation value: {correlation_value:.3f} (values close to 1.0 indicate strong positive correlation, close to -1.0 indicate strong negative correlation)

Example format (plain text, no markdown):
{target_name}: A ~2 year cycle is observed. Prices are currently trending upward. Correlated material shows lagging behavior.
{correlated_name}: No clear cycle is observed. Prices are currently trending upward. A significant price anomaly occurred in mid-2023.
General Insights: {target_name} and {correlated_name} show some correlation in price movements, with {target_name} leading.

Here is the data:
{data_text}

Provide the analysis in plain text format (no markdown, no asterisks, no hash symbols).
"""
        
        response = invoke_bedrock_text(system_msg, prompt, temperature=0.3, max_tokens=512)
        
        if not response or not response.strip():
            return "Unable to generate key takeaways at this time."
        
        # Clean up any markdown formatting that might have slipped through
        cleaned_response = response.strip()
        # Remove markdown bold (**text** becomes text)
        cleaned_response = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_response)
        # Remove standalone asterisks
        cleaned_response = cleaned_response.replace('**', '')
        # Remove markdown headers at start of lines (## or #)
        lines = cleaned_response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Remove leading # or ##
            line = re.sub(r'^#+\s*', '', line)
            if line:
                cleaned_lines.append(line)
        cleaned_response = '\n'.join(cleaned_lines)
        
        return cleaned_response
    except Exception as e:
        print(f"Error generating key takeaways: {e}")
        return "Unable to generate key takeaways at this time."


def get_material_correlations(target_material_id: str) -> Dict[str, Any]:
    """Get correlation data and key takeaways for a target material."""
    try:
        print(f"Fetching price history for material: {target_material_id}")
        
        # Fetch all price history data
        df = fetch_material_price_history()
        
        if df is None or df.empty:
            return {
                "success": False,
                "error": "No price history data found"
            }
        
        print(f"Fetched {len(df)} rows from price_history_data")
        
        # Process the data
        processed_df = process_price_data(df)
        
        if processed_df.empty:
            return {
                "success": False,
                "error": "No valid price data after processing"
            }
        
        # Debug: Check what material_ids are in the data
        unique_material_ids = list(processed_df['material_id'].unique())
        print(f"[DEBUG] Unique material_ids in data: {unique_material_ids}")
        print(f"[DEBUG] Looking for target_material_id: {target_material_id}")
        
        # Check if target material exists (case-insensitive and with/without leading zeros)
        target_found = False
        actual_target_id = target_material_id
        for mat_id in unique_material_ids:
            if str(mat_id).strip().upper() == str(target_material_id).strip().upper():
                actual_target_id = mat_id
                target_found = True
                print(f"[DEBUG] Found matching material_id: {actual_target_id}")
                break
        
        if not target_found:
            # Try to find similar material IDs (handle leading zeros)
            target_upper = str(target_material_id).strip().upper()
            for mat_id in unique_material_ids:
                mat_id_str = str(mat_id).strip().upper()
                # Try removing leading zeros or adding them
                if mat_id_str.replace('0', '') == target_upper.replace('0', '') or \
                   mat_id_str == target_upper.lstrip('0') or \
                   target_upper == mat_id_str.lstrip('0'):
                    actual_target_id = mat_id
                    target_found = True
                    print(f"[DEBUG] Found similar material_id: {actual_target_id} (was looking for {target_material_id})")
                    break
        
        if not target_found:
            return {
                "success": False,
                "error": f"Material {target_material_id} not found in price history data. Available materials: {unique_material_ids[:10]}..." if len(unique_material_ids) > 10 else f"Material {target_material_id} not found in price history data. Available materials: {unique_material_ids}"
            }
        
        # Calculate correlations using the actual material_id found
        most_correlated_id, correlation_value, all_correlations = calculate_correlations(
            processed_df, actual_target_id
        )
        
        if most_correlated_id is None:
            return {
                "success": False,
                "error": f"No correlation data found for material {target_material_id}"
            }
        
        # Get material names
        unique_material_ids = list(processed_df['material_id'].unique())
        material_names = {}
        for mat_id in unique_material_ids:
            name = get_material_name(mat_id)
            material_names[mat_id] = name if name else mat_id
        
        # Filter data for target and most correlated materials
        # Use actual_target_id (the one found in the database) instead of target_material_id
        analysis_materials = [actual_target_id, most_correlated_id]
        analysis_df = processed_df[processed_df['material_id'].isin(analysis_materials)]
        
        # Format data for Bedrock
        data_text = format_data_for_bedrock(analysis_df, material_names)
        
        # Generate key takeaways
        # Use actual_target_id to ensure correct material name lookup
        key_takeaways = generate_key_takeaways(
            data_text, 
            material_names, 
            actual_target_id,
            most_correlated_id,
            correlation_value
        )
        
        return {
            "success": True,
            "target_material_id": target_material_id,
            "target_material_name": material_names.get(actual_target_id, target_material_id),
            "most_correlated_material_id": most_correlated_id,
            "most_correlated_material_name": material_names.get(most_correlated_id, most_correlated_id),
            "correlation_value": float(correlation_value) if correlation_value is not None else None,
            "all_correlations": all_correlations,
            "key_takeaways": key_takeaways,
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in get_material_correlations: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def lambda_handler(event, context=None):
    """Lambda handler for correlation analysis."""
    try:
        print("Received event:", json.dumps(event, indent=2))
        
        # Extract material_id from event
        material_id = None
        if isinstance(event, dict):
            if 'body' in event and isinstance(event['body'], str):
                try:
                    body = json.loads(event['body'])
                    material_id = body.get('material_id')
                except Exception:
                    pass
            elif 'material_id' in event:
                material_id = event['material_id']

        if not material_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "success": False,
                    "error": "material_id parameter is required"
                })
            }
        
        print(f"Processing material_id: {material_id}")
        
        # Get correlation data and key takeaways
        result = get_material_correlations(material_id)
        
        if not result.get("success"):
            return {
                "statusCode": 404,
                "body": json.dumps(result)
            }

        return {
            "statusCode": 200,
            "body": json.dumps(result, indent=2)
        }
        
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": f"Lambda execution failed: {str(e)}"
            })
        }


# For local testing
if __name__ == "__main__":
    # Example local test
    result = get_material_correlations('102089-000000')
    print(json.dumps(result, indent=2))

