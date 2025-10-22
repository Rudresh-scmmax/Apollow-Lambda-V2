from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import boto3
from db_query import database_query

# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ARNs
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"

def get_material_data(material_id: str) -> List[Dict]:
    """Get material price history data from news_insights table"""
    query = """
        SELECT material_id, published_date::text, title, source, news_tag
        FROM news_insights 
        WHERE material_id = %s
        ORDER BY published_date DESC
    """
    result = database_query(query, [material_id])
    print(f"Raw result from database_query: {result}")
    
    # Check for errors first
    if isinstance(result, dict) and result.get('statusCode') == 500:
        print(f"Database query error: {result.get('body')}")
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
            body = json.loads(result["body"])
        except json.JSONDecodeError:
            print(f"Failed to parse body: {result['body']}")
            return []
    else:
        body = result
    
    if not isinstance(body, list):
        print(f"Expected list but got: {type(body)} - {body}")
        return []
    
    data = []
    for row in body:
        data.append({
            'material_id': row.get('material_id'),
            'published_date': row.get('published_date', ''),
            'title': row.get('title', ''),
            'source': row.get('source', ''),
            'news_tag': row.get('news_tag', '')
        })
    return data

def get_takeaways(material_id: str) -> List[Dict]:
    """Get takeaways from material_research_reports table"""
    query = """
        SELECT publication, report_link, published_date::text, material_id, takeaway 
        FROM material_research_reports 
        WHERE material_id = %s
        ORDER BY published_date DESC
    """
    result = database_query(query, [material_id])
    print(f"Takeaways raw result: {result}")
    
    # Check for errors first
    if isinstance(result, dict) and result.get('statusCode') == 500:
        print(f"Database query error: {result.get('body')}")
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
            body = json.loads(result["body"])
        except json.JSONDecodeError:
            print(f"Failed to parse body: {result['body']}")
            return []
    else:
        body = result
    
    if not isinstance(body, list):
        print(f"Expected list but got: {type(body)} - {body}")
        return []
    
    data = []
    for row in body:
        data.append({
            'publication': row.get('publication', ''),
            'report_link': row.get('report_link', ''),
            'published_date': row.get('published_date', ''),
            'material_id': row.get('material_id', ''),
            'takeaway': row.get('takeaway', '')
        })
    return data

def get_material_name(material_id: str) -> Optional[str]:
    """Get material description from material_master table"""
    query = """
        SELECT material_description
        FROM material_master
        WHERE material_id = %s
        LIMIT 1
    """
    result = database_query(query, [material_id])
    print(f"Material name raw result: {result}")
    
    # Check for errors first
    if isinstance(result, dict) and result.get('statusCode') == 500:
        print(f"Database query error: {result.get('body')}")
        return None
    
    # Handle different response formats
    if isinstance(result, str):
        try:
            body = json.loads(result)
        except json.JSONDecodeError:
            print(f"Failed to parse string result: {result}")
            return None
    elif isinstance(result, dict) and "body" in result:
        try:
            body = json.loads(result["body"])
        except json.JSONDecodeError:
            print(f"Failed to parse body: {result['body']}")
            return None
    else:
        body = result
    
    if not isinstance(body, list):
        print(f"Expected list but got: {type(body)} - {body}")
        return None
    
    if body and len(body) > 0:
        return body[0].get('material_description')
    return None

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

def analyze_with_bedrock(material_id: str, material_name: Optional[str], material_data: List[Dict], takeaways: List[Dict]) -> Dict:
    material_display_name = material_name if material_name else material_id
    
    system_msg = """You are an expert business strategy analyst. Analyze the provided data and provide a comprehensive Porter's Five Forces analysis."""
    
    user_content = f"""
Analyze the following data for {material_display_name} and provide a Porter's Five Forces analysis.

News Insights Data: {json.dumps(material_data, indent=2)}
Market Research Takeaways: {json.dumps(takeaways, indent=2)}

Based on this data, provide a comprehensive Porter's Five Forces analysis.

Return your analysis in this exact JSON format:
{{
    "material_name": "{material_display_name}",
    "threat_of_substitution": {{
        "intensity": "Low/Medium/High",
        "description": "Analysis of substitute products for {material_display_name}",
        "factors": ["factor1", "factor2", "factor3"]
    }},
    "bargaining_power_suppliers": {{
        "intensity": "Low/Medium/High", 
        "description": "Analysis of supplier power for {material_display_name}",
        "factors": ["factor1", "factor2", "factor3"]
    }},
    "bargaining_power_buyers": {{
        "intensity": "Low/Medium/High",
        "description": "Analysis of buyer power for {material_display_name}", 
        "factors": ["factor1", "factor2", "factor3"]
    }},
    "competitive_rivalry": {{
        "intensity": "Low/Medium/High",
        "description": "Analysis of competition in the {material_display_name} market",
        "factors": ["factor1", "factor2", "factor3"]
    }},
    "threat_new_entrants": {{
        "intensity": "Low/Medium/High",
        "description": "Analysis of entry barriers in the {material_display_name} market",
        "factors": ["factor1", "factor2", "factor3"]
    }},
    "summary": "Overall strategic assessment for {material_display_name}"
}}

Only return valid JSON. No markdown formatting.
"""
    
    result = invoke_bedrock_text(system_msg, user_content)
    
    # invoke_bedrock_text now returns parsed JSON or None
    if result is not None:
        return result
    else:
        # Fallback if analysis fails
        return {
            "material_name": material_display_name,
            "threat_of_substitution": {"intensity": "Medium", "description": "Analysis not available", "factors": []},
            "bargaining_power_suppliers": {"intensity": "Medium", "description": "Analysis not available", "factors": []},
            "bargaining_power_buyers": {"intensity": "Medium", "description": "Analysis not available", "factors": []},
            "competitive_rivalry": {"intensity": "Medium", "description": "Analysis not available", "factors": []},
            "threat_new_entrants": {"intensity": "Medium", "description": "Analysis not available", "factors": []},
            "summary": "Analysis generation failed"
        }

def generate_porters_analysis_and_save(material_id: str) -> Dict[str, Any]:
    material_data = get_material_data(material_id)
    print(f"material_data: {material_data}")
    takeaways = get_takeaways(material_id)
    material_name = get_material_name(material_id)

    if not material_data and not takeaways:
        raise Exception(f"No data found for material {material_id}")

    analysis_result = analyze_with_bedrock(material_id, material_name, material_data, takeaways)

    # Save to DB using the correct table structure
    analysis_json = json.dumps(analysis_result)
    analysis_date = datetime.now().date().isoformat()
    
    # Insert or update porters_analysis table
    query = """
        INSERT INTO porters_analysis ( material_id, analysis_json, analysis_date, created_at, updated_at)
        VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_DATE)
        ON CONFLICT (id) DO UPDATE SET
            analysis_json = EXCLUDED.analysis_json,
            analysis_date = EXCLUDED.analysis_date,
            updated_at = CURRENT_DATE;
        """
    
    result = database_query(query, [material_id, analysis_json, analysis_date])
    print(f"Saved Porter's analysis to database: {result}")
    
    # Check if save was successful
    if isinstance(result, str):
        result_data = json.loads(result)
    elif isinstance(result, dict) and "body" in result:
        result_data = json.loads(result["body"])
    else:
        result_data = result
    
    print(f"Save operation result: {result_data}")

    return {
        "success": True,
        "material_id": material_id,
        "material_name": material_name or material_id,
        "material_analyzed": material_name if material_name else material_id,
        "analysis_date": analysis_date,
        "porters_analysis": analysis_result,
        "data_points": {
            "news_insights": len(material_data),
            "takeaways": len(takeaways),
        },
        "error": None,
    }

def lambda_handler(event, context):
    material_id = event.get('material_id')
    if not material_id:
        return {
            "success": False,
            "error": "material_id parameter is required"
        }

    try:
        result = generate_porters_analysis_and_save(material_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "material_id": material_id,
            "error": str(e)
        }


if __name__ == "__main__":
    result = lambda_handler({"material_id": "100724-000000"}, None)
    print(result)