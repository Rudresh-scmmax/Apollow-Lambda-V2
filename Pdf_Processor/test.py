import boto3
import time
from PIL import Image
from io import BytesIO

# ==== CONFIG ====
REGION = "us-east-1"
MODEL_ID = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama3-2-11b-instruct-v1:0"

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def query_bedrock_with_image(image_path, max_retries=3, retry_delay=5):
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
                modelId=MODEL_ID,
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

text = query_bedrock_with_image("page_0_part0.png")

# Print the first few lines
print("\n--- Extracted Text ---\n")
print(text)

# Test price extraction functionality
def test_price_extraction():
    """Test the price extraction and upsert functionality"""
    from extract_market_intelligence import DatabaseManager
    
    # Sample extracted text with price information
    sample_text = """
    Ethylene prices in Asia-Pacific region have shown significant volatility.
    Current spot prices are $850-900 per metric ton as of 2024-01-15.
    Contract prices for Q1 2024 are expected to be $880-920 per MT.
    European ethylene prices remain stable at $820-850 per MT.
    """
    
    print("\n--- Testing Price Extraction ---")
    try:
        db = DatabaseManager()
        result = db.extract_and_upsert_prices(
            sample_text,
            "Ethylene",
            "102089-000000",  # Sample material_id
            "212"  # Sample location_id
        )
        
        print(f"Price extraction result: {result}")
        
        if result.get("success"):
            print(f"✅ Successfully processed {result['processed_count']}/{result['total_entries']} price entries")
        else:
            print(f"❌ Price extraction failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

# Test supplier shutdowns extraction functionality
def test_supplier_shutdowns_extraction():
    """Test the supplier shutdowns extraction and upsert functionality"""
    from extract_market_intelligence import DatabaseManager
    
    # Sample extracted text with supplier shutdown information
    sample_text = """
    Major ethylene producer BASF announced a planned shutdown of their Ludwigshafen plant 
    from 2024-03-15 to 2024-04-30 for maintenance. This will impact regional supply 
    significantly. Dow Chemical also reported an unplanned shutdown at their Texas facility 
    starting 2024-02-20 due to equipment failure, with restart expected by 2024-03-10.
    """
    
    print("\n--- Testing Supplier Shutdowns Extraction ---")
    try:
        db = DatabaseManager()
        result = db.extract_and_upsert_supplier_shutdowns(
            sample_text,
            "Ethylene",
            "102089-000000",  # Sample material_id
            "212",  # Sample location_id
            "https://example.com/report",  # Sample report URL
            1  # Sample user_id
        )
        
        print(f"Supplier shutdowns extraction result: {result}")
        
        if result.get("success"):
            print(f"✅ Successfully processed {result['processed_count']}/{result['total_entries']} shutdown entries")
        else:
            print(f"❌ Supplier shutdowns extraction failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

# Run the tests
test_price_extraction()
test_supplier_shutdowns_extraction()