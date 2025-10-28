import os
import json
import boto3
import uuid
import fitz  # PyMuPDF


# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
s3 = boto3.client("s3")

# Model ARNs
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"
IMAGE_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama3-2-11b-instruct-v1:0"

# Llama 3.2 11B Vision model has a pixel limit of approximately 1568x1568
MAX_IMAGE_DIMENSION = 1568


def query_bedrock_with_image(image_path, max_retries=3, retry_delay=5):
    print(f"image_path: {image_path}")
    """
    Extract text from an image using Bedrock's Llama 3.2 vision model via Converse API.
    Uses the same approach as the Node.js implementation.
    """
    import time
    
    for attempt in range(1, max_retries + 1):
        try:
            # Read image as bytes
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Determine image format from file extension
            image_format = "png" if image_path.lower().endswith('.png') else "jpeg"
            
            # Build the prompt (matching Node.js version)
            prompt = "Transcribe all text from this image in **markdown** format. Capture every visible word, including small print, headers, footnotes, and tables."
            
            # Construct messages for Converse API
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt},
                        {
                            "image": {
                                "format": image_format,
                                "source": {"bytes": image_bytes}
                            }
                        }
                    ]
                }
            ]
            
            # Call Converse API
            response = bedrock.converse(
                modelId=IMAGE_MODEL_ARN,
                messages=messages,
                inferenceConfig={
                    "maxTokens": 2048,
                    "temperature": 0,
                    "topP": 0.1
                }
            )
            
            # Extract text from response
            text = ""
            if response.get('output') and response['output'].get('message'):
                content = response['output']['message'].get('content', [])
                if content and len(content) > 0:
                    text = content[0].get('text', '')
            
            print(f"Extracted {len(text)} characters from image")
            return text
            
        except Exception as e:
            error_name = type(e).__name__
            print(f"Bedrock image error (attempt {attempt}/{max_retries}): {e}")
            
            # Retry on throttling or service unavailable errors
            if error_name in ['ThrottlingException', 'ServiceUnavailableException'] and attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            elif attempt == max_retries:
                print("Error extracting text from image after multiple attempts.")
                return ""
            else:
                # For other errors, don't retry
                return ""
    
    return ""


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


def generate_takeaways(extracted_text: str, material: str) -> str:
    """
    Extract key takeaways (6–8 points, no char limit) for a given material.
    """
    system_msg = f"""
    You are a helpful assistant that extracts key takeaways from market research reports.
    Your task is to:
    1. Identify and extract the publication (e.g., ICIS, Chem Analyst, etc.). If not found, use "Unknown".
    2. Extract the published date and return it in YYYY-MM-DD format only. If the exact day is not available, use the first day of the month. If only the year is known, use "2023-01-01".
    3. The material of focus for this report is: "{material}".
    4. Summarize the report's most important findings and insights with 6–8 bullet points (use '-' for bullets, keep each clear and concise).
    5. Return the output in this EXACT JSON format:
    {{
        "publication": "publication name here",
        "published_date": "YYYY-MM-DD",
        "takeaway_list": [
            "- first takeaway",
            "- second takeaway",
            "- third takeaway"
        ]
    }}
    6. The key for takeaways MUST be "takeaway_list" (not "findings", "summary", or anything else).
    7. Return pure JSON only. No markdown or explanation.
    """
    data = invoke_bedrock_text(system_msg.strip(), extracted_text.strip())
    
    # Normalize the response to ensure takeaway_list key
    if data:
        if not data.get("publication"):
            data["publication"] = "Unknown"
        
        # Normalize different possible keys to "takeaway_list"
        if "takeaway_list" not in data:
            for possible_key in ["findings", "summary", "takeaways", "key_points", "insights"]:
                if possible_key in data:
                    data["takeaway_list"] = data.pop(possible_key)
                    break
        
        # If still no takeaway_list, create an empty one
        if "takeaway_list" not in data:
            data["takeaway_list"] = []
    
    return json.dumps(data) if data else json.dumps({"publication": "Unknown", "takeaway_list": [], "error": "Failed to extract"})


def news_agent(extracted_text, material, report_url):
    """
    Extract specific news related to the material and detect the main region from the text.
    
    Returns:
        A list of news dicts, or an empty list if none found.
    """
    system_msg = f"""
    You are a helpful assistant extracting market-related news from a report about '{material}'.

    For each news item:
    - Extract a short, specific headline ("title")
    - Extract the date ("published_date") in YYYY-MM-DD
    - Extract the **main region** relevant to the news ("region"). 
      If multiple regions are mentioned, return only the primary region (e.g., 'Asia-Pacific' from 'China, India, Asia-Pacific').
    - Always include "material": '{material}'
    - Include "news_url"; if not available, use fallback {report_url}

    Only return actual news events, ignore headings or summaries.

    Respond strictly in a JSON list.
    """
    
    try:
        news_list = invoke_bedrock_text(system_msg.strip(), extracted_text.strip())
        if not isinstance(news_list, list):
            return []
        
        cleaned_news = []
        for item in news_list:
            title = item.get("title", "").strip()
            if not title:
                continue
            
            item["news_url"] = item.get("news_url") or report_url
            item["material"] = material
            # Ensure only main region is returned
            region = item.get("region")
            if region:
                item["region"] = region.split(",")[-1].strip()
            
            cleaned_news.append(item)
        
        return cleaned_news
    except Exception as e:
        print(f"[ERROR] Failed to extract news: {e}")
        return []


def classify_news_tags(news_item):
    """
    Classify a news item and extract the most relevant tag/category.
    
    Args:
        news_item: Dict containing news item with 'title' and optionally 'description'
    
    Returns:
        String representing the most relevant tag/category, or empty string if none found
    """
    title = news_item.get('title', '')
    description = news_item.get('description', '')
    
    system_msg = """You are a news classifier. Analyze the news and return ONLY the exact tag name from these categories:

Available categories:
- "Plant Closure": Plant shutdowns, breakdowns, maintenance, outages
- "Force Majeure": Natural disasters, strikes, uncontrollable events  
- "Taxes": Tax changes, tariffs, duties, import/export taxes
- "Rule Changes": Regulatory changes, new regulations, policy changes

IMPORTANT: Return ONLY the tag name in quotes (e.g., "Plant Closure") or return "none" if no category matches.

Do NOT include any explanations, reasoning, or additional text. Just the tag name or "none"."""

    user_content = f"News title: {title}"
    if description:
        user_content += f"\nDescription: {description}"
    
    try:
        result = invoke_bedrock_text(system_msg.strip(), user_content.strip())
        if isinstance(result, str):
            # Clean the result to extract just the tag name
            result = result.strip()
            
            # Remove any explanatory text and extract just the tag
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1]  # Remove quotes
            elif result.startswith("Therefore, the most relevant tag for this news item is: "):
                # Handle the case where LLM returns explanatory text
                result = result.replace("Therefore, the most relevant tag for this news item is: ", "").strip()
                if result.startswith('"') and result.endswith('"'):
                    result = result[1:-1]
            
            # Check if it's one of the valid categories
            valid_tags = ["Plant Closure", "Force Majeure", "Taxes", "Rule Changes"]
            if result in valid_tags:
                return result
            else:
                return ""
        else:
            return ""
    except Exception as e:
        print(f"[ERROR] Failed to classify news tags: {e}")
        return ""


def price_outlook_agent(extracted_text, material):
    """
    Extract price outlook related to the material and detect the main region from the text.
    """
    system_msg = f"""
    You are a helpful assistant analyzing the price outlook for '{material}'.

    Extract the following fields for the **main region** only:
    - "region": Return only the primary/main region even if multiple are mentioned.
    - "price_trend": One of "increasing", "decreasing", or "stable"
    - "key_factors": List of key drivers influencing the price
    - "short_term_outlook": 1–3 sentence summary of short-term price expectations
    - "long_term_outlook": 1–3 sentence summary of long-term price expectations

    Do NOT include explanations outside the JSON.
    If no price outlook is found, return: null
    """
    result = invoke_bedrock_text(system_msg, extracted_text)
    if result and isinstance(result, dict) and "region" in result:
        result["region"] = result["region"].split(",")[-1].strip()
    return result


def extract_demand_supply_outlook_agent(extracted_text: str, material: str):
    """
    Detect and extract demand and/or supply outlook-related information and the main region.
    """
    system_msg = f"""
    You are an expert market analyst extracting demand and supply outlooks for '{material}'.

    For each outlook item:
    - Include "impact_text", "published_date" (YYYY-MM-DD), "source_link" if mentioned.
    - Extract **only the main region** ("region") for each item. If multiple regions are mentioned, return the primary/main one (e.g., 'Asia-Pacific' from 'China, India, Asia-Pacific').
    - Include "material": '{material}'

    Return a JSON object with two top-level keys: "demand" and "supply", each mapping to a list of items.
    Respond strictly in JSON, no explanations.
    """
    
    llm_raw_result = invoke_bedrock_text(system_msg, extracted_text)
    
    parsed_data = {"demand": [], "supply": []}
    try:
        if isinstance(llm_raw_result, str):
            parsed_data = json.loads(llm_raw_result)
        elif isinstance(llm_raw_result, dict):
            parsed_data = llm_raw_result
        
        def clean_list(items):
            final_list = []
            for item in items:
                if isinstance(item, dict):
                    item["material"] = material
                    region = item.get("region")
                    if region:
                        item["region"] = region.split(",")[-1].strip()
                    final_list.append(item)
            return final_list
        
        return {
            "demand": clean_list(parsed_data.get("demand", [])),
            "supply": clean_list(parsed_data.get("supply", [])),
        }
        
    except Exception as e:
        print(f"Parsing error: {e}. Raw LLM output: {llm_raw_result}")
        return {"demand": [], "supply": []}


def supplier_shutdowns_agent(extracted_text, material):
    """
    Extract supplier shutdown events and detect the main region.
    """
    system_msg = f"""
    You are a helpful assistant that extracts supplier shutdown events for the material '{material}'.
    
    For each event:
    - Include "producer", "shutdown_from", "shutdown_to", "impact", "key_takeaway"
    - Extract **only the main region** ("region"). If multiple regions are mentioned, return the primary one.
    - Include "material": '{material}'
    
    Respond strictly in JSON.
    """
    shutdowns = invoke_bedrock_text(system_msg, extracted_text)
    
    if not isinstance(shutdowns, list):
        return []
    
    for event in shutdowns:
        event["material"] = material
        region = event.get("region")
        if region:
            event["region"] = region.split(",")[-1].strip()
    
    return shutdowns


def price_by_date_agent(extracted_text, material):
    """
    Extracts price data by date and detects the main region.
    """
    system_msg = f"""
    You are a helpful assistant extracting historical and current price data for '{material}'.

    For each price entry:
    - Include "date", "price", "price_type", "unit"
    - Extract **only the main region** ("region"). If multiple regions are mentioned, return the primary one.
    - Include "material": '{material}'
    - Include optional fields if available: "capacity_utilization", "demand_outlook", "supply_disruption", "business_cycle"

    Return strictly a JSON list.
    """
    price_list = invoke_bedrock_text(system_msg, extracted_text)
    
    if not isinstance(price_list, list):
        return []
    
    for price in price_list:
        price["material"] = material
        region = price.get("region")
        if region:
            price["region"] = region.split(",")[-1].strip()
    
    return price_list




def summarize_demand_supply_with_bedrock(demand_data, supply_data, material_id, location_id, summary_date):
    """
    Uses AWS Bedrock to summarize demand and supply data.
    
    Args:
        demand_data (list): List of demand impact records
        supply_data (list): List of supply impact records
        material_id (str): Material ID
        location_id (int): Location ID
        summary_date (str): Summary date
        
    Returns:
        dict: Contains summarized text for demand, supply, and combined
    """
    try:
        # Prepare data for summarization
        demand_texts = [item.get('demand_impact', '') for item in demand_data if item.get('demand_impact')]
        supply_texts = [item.get('supply_impact', '') for item in supply_data if item.get('supply_impact')]
        
        # Create context for Bedrock
        context = f"""
        Material ID: {material_id}
        Location ID: {location_id}
        Summary Date: {summary_date}
        
        DEMAND IMPACT DATA:
        {chr(10).join([f"- {text}" for text in demand_texts]) if demand_texts else "No demand data available"}
        
        SUPPLY IMPACT DATA:
        {chr(10).join([f"- {text}" for text in supply_texts]) if supply_texts else "No supply data available"}
        """
        
        system_msg = """
        You are an expert market analyst that creates concise summaries of demand and supply impact data.
        
        Your task is to:
        1. Create a clear, concise demand summary (2-3 sentences max)
        2. Create a clear, concise supply summary (2-3 sentences max)  
        3. Create a combined summary that shows the overall market outlook (2-3 sentences max)
        
        Focus on:
        - Key trends and patterns
        - Market sentiment (positive/negative/neutral)
        - Important factors affecting the market
        - Overall outlook for the material and location
        
        Return your response in this EXACT JSON format:
        {
            "demand_summary": "Your demand summary here",
            "supply_summary": "Your supply summary here", 
            "combined_summary": "Your combined market outlook here"
        }
        
        Keep summaries professional, factual, and actionable.
        """
        
        result = invoke_bedrock_text(system_msg, context)
        
        if result and isinstance(result, dict):
            return {
                'demand_summary': result.get('demand_summary', 'No demand data available for summarization'),
                'supply_summary': result.get('supply_summary', 'No supply data available for summarization'),
                'combined_summary': result.get('combined_summary', 'Insufficient data for market outlook')
            }
        else:
            # If invoke_bedrock_text returns None due to JSON parsing error, try manual parsing
            try:
                # Get the raw response and extract JSON manually
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"text": context.strip()}
                        ]
                    }
                ]
                
                response = bedrock.converse(
                    modelId=TEXT_MODEL_ARN,
                    messages=messages,
                    system=[{"text": system_msg.strip()}],
                    inferenceConfig={
                        "maxTokens": 4096,
                        "temperature": 0.1,
                        "topP": 0.9
                    }
                )
                
                # Extract text from response
                text = ""
                if response.get('output') and response['output'].get('message'):
                    content = response['output']['message'].get('content', [])
                    if content and len(content) > 0:
                        text = content[0].get('text', '')
                
                # Clean up the response text
                text = text.replace("```json", "").replace("```", "").strip()
                
                # Try to find JSON in the response
                if "{" in text and "}" in text:
                    # Find the JSON part
                    start_idx = text.find("{")
                    end_idx = text.rfind("}") + 1
                    json_text = text[start_idx:end_idx]
                    
                    # Parse the JSON
                    parsed_result = json.loads(json_text)
                    
                    return {
                        'demand_summary': parsed_result.get('demand_summary', 'No demand data available for summarization'),
                        'supply_summary': parsed_result.get('supply_summary', 'No supply data available for summarization'),
                        'combined_summary': parsed_result.get('combined_summary', 'Insufficient data for market outlook')
                    }
                else:
                    raise ValueError("No JSON found in response")
                    
            except Exception as parse_error:
                print(f"[ERROR] Manual JSON parsing failed: {parse_error}")
                return {
                    'demand_summary': 'No demand data available for summarization',
                    'supply_summary': 'No supply data available for summarization', 
                    'combined_summary': 'Insufficient data for market outlook'
                }
            
    except Exception as e:
        print(f"[ERROR] Failed to summarize with Bedrock: {e}")
        return {
            'demand_summary': 'Error in summarization',
            'supply_summary': 'Error in summarization',
            'combined_summary': 'Error in summarization'
        }