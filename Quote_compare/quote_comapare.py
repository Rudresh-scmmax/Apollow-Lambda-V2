import json
import os
import base64
import PyPDF2
from openpyxl import Workbook
from datetime import date, datetime
import re
from io import BytesIO
import boto3
import requests
import http.client
from typing import Optional
from rapidfuzz import process, fuzz
from db_query import database_query

# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"

class DatabaseManager:
    def __init__(self):
        pass

    def _parse_db_result(self, result):
        """Helper to parse database_query results"""
        print(f"[DEBUG] _parse_db_result received: type={type(result)}, value={result}")
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

    def _get_material_id(self, material: Optional[str], score_cutoff: int = 80) -> Optional[str]:
        """Return the best-matching material_id using RapidFuzz.
        Case-insensitive matching: handles mixed case in database (e.g., 'Glycerine' matches 'GLYCERINE')."""
        if not material:
            return None

        query = "SELECT material_id, material_description FROM material_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        choices = {r["material_description"]: r["material_id"] for r in rows}

        best = process.extractOne(
            material,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None

    def _get_supplier_id(self, supplier: Optional[str], score_cutoff: int = 80) -> Optional[int]:
        """Return the best-matching supplier_id using RapidFuzz.
        Case-insensitive matching: handles mixed case in database (e.g., 'ABC Company' matches 'abc company').
        Matches against both supplier_name and supplier_plant_name."""
        if not supplier:
            return None

        query = "SELECT supplier_id, supplier_name, supplier_plant_name FROM supplier_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        # Create choices from both supplier_name and supplier_plant_name
        choices = {}
        for r in rows:
            if r.get("supplier_name"):
                choices[r["supplier_name"]] = r["supplier_id"]
            if r.get("supplier_plant_name"):
                choices[r["supplier_plant_name"]] = r["supplier_id"]

        best = process.extractOne(
            supplier,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None

    def _get_currency_id(self, currency_name: Optional[str], score_cutoff: int = 80) -> Optional[int]:
        """Return the best-matching currency_id using RapidFuzz.
        Case-insensitive matching: handles mixed case in database (e.g., 'US Dollar' matches 'us dollar').
        Also handles currency codes like 'USD' matching 'US Dollar'."""
        if not currency_name:
            return None

        query = "SELECT currency_id, currency_name FROM currency_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        choices = {r["currency_name"]: r["currency_id"] for r in rows}

        best = process.extractOne(
            currency_name,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None

    def _get_country_id(self, country_name: Optional[str], score_cutoff: int = 80) -> Optional[int]:
        """Return the best-matching country_id using RapidFuzz.
        Case-insensitive matching: handles mixed case in database (e.g., 'United States' matches 'UNITED STATES')."""
        if not country_name:
            return None

        query = "SELECT country_id, country_name FROM country_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        choices = {r["country_name"]: r["country_id"] for r in rows}

        best = process.extractOne(
            country_name,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None

    def insert_quotation(self, material_code, vendor_name, price_per_unit, currency, country_of_origin, 
                        user_id, pdf_key=None, batch_id=None, quote_date=None):
        """Insert quotation into quote_comparison table."""
        try:
            # Get IDs from names
            material_id = self._get_material_id(material_code)
            supplier_id = self._get_supplier_id(vendor_name)
            currency_id = self._get_currency_id(currency)
            
            # Get country_id from first country if multiple
            country_names = [c.strip() for c in country_of_origin.split(",")] if country_of_origin else []
            country_id = None
            if country_names:
                country_id = self._get_country_id(country_names[0])

            if not material_id:
                print(f"[WARNING] Could not find material_id for: {material_code}")
                return False
            if not supplier_id:
                print(f"[WARNING] Could not find supplier_id for: {vendor_name}")
                return False
            if not currency_id:
                print(f"[WARNING] Could not find currency_id for: {currency}")
                return False
            if not country_id:
                print(f"[ERROR] Could not find country_id for: {country_of_origin}")
                return False

            # Use provided quote_date or current date
            if quote_date:
                if isinstance(quote_date, str):
                    quote_date_str = quote_date
                elif isinstance(quote_date, date):
                    quote_date_str = quote_date.isoformat()
                else:
                    quote_date_str = date.today().isoformat()
            else:
                quote_date_str = date.today().isoformat()

            # Convert price to decimal
            try:
                price_value = float(price_per_unit)
            except (ValueError, TypeError):
                print(f"[ERROR] Invalid price_per_unit: {price_per_unit}")
                return False

            query = """
                INSERT INTO quote_comparison (
                    material_id, supplier_id, price_per_unit, currency_id, country_id,
                    quote_date, user_id, pdf_key, batch_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            result = database_query(query, [
                material_id,
                supplier_id,
                price_value,
                currency_id,
                country_id,
                quote_date_str,
                user_id,
                pdf_key,
                batch_id
            ])

            if isinstance(result, dict) and result.get('statusCode') == 500:
                print(f"[ERROR] Failed to insert quotation: {result.get('error')}")
                return False

            print(f"[SUCCESS] Quotation inserted: {vendor_name} - {material_code}")
            return True
        except Exception as e:
            print(f"[ERROR] Error inserting quotation: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return False

    def fetch_country_tariffs(self):
        """Fetch tariff percentages by country name from country_tariffs table."""
        try:
            query = """
                SELECT c.country_name, ct.tariff_percentage 
                FROM country_tariffs ct
                JOIN country_master c ON ct.country_id = c.country_id
            """
            result = database_query(query)
            rows = self._parse_db_result(result)
            
            tariffs = {}
            for row in rows:
                name = (row.get("country_name") or "").strip().lower()
                percentage = row.get("tariff_percentage")
                try:
                    tariffs[name] = float(percentage)
                except (TypeError, ValueError):
                    continue
            return tariffs
        except Exception as e:
            print(f"[ERROR] Error fetching country tariffs: {e}")
            return {}

    def generate_excel_report_from_db(self, batch_id=None, filename='quotations_report.xlsx'):
        """Generate Excel report from quote_comparison table."""
        try:
            if batch_id:
                query = """
                    SELECT 
                        m.material_description as material_code,
                        s.supplier_name as vendor_name,
                        qc.price_per_unit,
                        c.currency_name as currency,
                        co.country_name as country_of_origin,
                        qc.quote_date
                    FROM quote_comparison qc
                    JOIN material_master m ON qc.material_id = m.material_id
                    JOIN supplier_master s ON qc.supplier_id = s.supplier_id
                    JOIN currency_master c ON qc.currency_id = c.currency_id
                    LEFT JOIN country_master co ON qc.country_id = co.country_id
                    WHERE qc.batch_id = %s
                """
                result = database_query(query, [batch_id])
            else:
                query = """
                    SELECT 
                        m.material_description as material_code,
                        s.supplier_name as vendor_name,
                        qc.price_per_unit,
                        c.currency_name as currency,
                        co.country_name as country_of_origin,
                        qc.quote_date
                    FROM quote_comparison qc
                    JOIN material_master m ON qc.material_id = m.material_id
                    JOIN supplier_master s ON qc.supplier_id = s.supplier_id
                    JOIN currency_master c ON qc.currency_id = c.currency_id
                    LEFT JOIN country_master co ON qc.country_id = co.country_id
                """
                result = database_query(query)
            
            rows = self._parse_db_result(result)

            wb = Workbook()
            ws = wb.active
            ws.title = "Quotations"
            ws.append(['Material Code', 'Vendor', 'Price/Unit', 'Currency', 'Country of Origin', 'Quote Date'])
            for row in rows:
                ws.append([
                    row.get('material_code', ''),
                    row.get('vendor_name', ''),
                    row.get('price_per_unit', 0),
                    row.get('currency', ''),
                    row.get('country_of_origin', ''),
                    row.get('quote_date', '')
                ])
            
            # Save to BytesIO for Lambda (no local file system)
            excel_buffer = BytesIO()
            wb.save(excel_buffer)
            excel_buffer.seek(0)
            
            print(f"[SUCCESS] Excel report generated with {len(rows)} records")
            return excel_buffer
        except Exception as e:
            print(f"[ERROR] Error generating Excel report: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return None

    def update_quotation_by_id(self, row_id, **fields):
        """Update quotation in quote_comparison table by id."""
        try:
            print(f"[DEBUG] update_quotation_by_id called with row_id={row_id}, fields={fields}")
            # Map old field names to new table structure if needed
            field_mapping = {
                'material_code': 'material_id',
                'vendor_name': 'supplier_id',
                'currency': 'currency_id',
                'country_of_origin': 'country_id'
            }
            
            # Convert names to IDs if needed
            update_fields = {}
            for key, value in fields.items():
                mapped_key = field_mapping.get(key, key)
                print(f"[DEBUG] Processing field: {key}={value} -> mapped_key={mapped_key}")
                
                if mapped_key == 'material_id' and key == 'material_code':
                    material_id = self._get_material_id(value)
                    print(f"[DEBUG] Material lookup: '{value}' -> material_id={material_id}")
                    if material_id:
                        update_fields['material_id'] = material_id
                elif mapped_key == 'supplier_id' and key == 'vendor_name':
                    supplier_id = self._get_supplier_id(value)
                    print(f"[DEBUG] Supplier lookup: '{value}' -> supplier_id={supplier_id}")
                    if supplier_id:
                        update_fields['supplier_id'] = supplier_id
                elif mapped_key == 'currency_id' and key == 'currency':
                    currency_id = self._get_currency_id(value)
                    print(f"[DEBUG] Currency lookup: '{value}' -> currency_id={currency_id}")
                    if currency_id:
                        update_fields['currency_id'] = currency_id
                elif mapped_key == 'country_id' and key == 'country_of_origin':
                    # Handle comma-separated countries
                    country_names = [c.strip() for c in value.split(",")] if value else []
                    print(f"[DEBUG] Country names parsed: {country_names}")
                    if country_names:
                        country_id = self._get_country_id(country_names[0])
                        print(f"[DEBUG] Country lookup: '{country_names[0]}' -> country_id={country_id}")
                        if country_id:
                            update_fields['country_id'] = country_id
                else:
                    update_fields[mapped_key] = value
            
            print(f"[DEBUG] Final update_fields: {update_fields}")

            if not update_fields:
                print("[WARNING] No valid fields to update")
                return False

            set_clause = ', '.join([f"{k} = %s" for k in update_fields.keys()])
            values = list(update_fields.values())
            values.append(row_id)
            
            query = f"UPDATE quote_comparison SET {set_clause} WHERE id = %s"
            result = database_query(query, values)
            
            if isinstance(result, dict) and result.get('statusCode') == 500:
                print(f"[ERROR] Failed to update quotation: {result.get('error')}")
                return False
            
            print(f"[SUCCESS] Updated quotation with id={row_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Error updating quotation: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return False

    def get_quotations_by_batch_id(self, batch_id):
        """Get all quotations for a given batch_id."""
        try:
            query = "SELECT id, pdf_key FROM quote_comparison WHERE batch_id = %s"
            result = database_query(query, [batch_id])
            rows = self._parse_db_result(result)
            return rows
        except Exception as e:
            print(f"[ERROR] Error fetching quotations by batch_id: {e}")
            return []

def g_search(query):
    """Perform a Google API search using the specified query."""
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        X_API_KEY = os.environ.get('SERPER_API_KEY', '362de99dbd1b66f05282fd62aa1aa832001047a2')

        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': X_API_KEY,
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        search_results = data.decode("utf-8")
        return search_results
    except Exception as e:
        print(f"Error in Google search: {e}")
        return "{}"


def invoke_bedrock_text(system_msg: str, user_content: str, temperature: float = 0.1, max_tokens: int = 1024):
    """
    Helper to call Bedrock text model and return raw string response.
    """
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

def search_material_price(raw_material):
    """Search for the current market price of the given raw material in USD."""
    search_result = g_search(f"What is the current market price for {raw_material} in USD?")
    return search_result

def process_price(input_text):
    """Extract price using AWS Bedrock."""
    try:
        system_msg = (
            "You are a procurement assistant. Extract a single representative unit price "
            "from the provided information. Respond with only the number (integer) without "
            "any additional text or currency symbols. If no price is found, return 0."
        )
        raw_response = invoke_bedrock_text(system_msg, input_text, temperature=0)
        if not raw_response:
            return "0"

        match = re.search(r"[-+]?\d+(?:\.\d+)?", raw_response.replace(",", ""))
        if match:
            value = match.group(0)
            # Return integer string if possible
            try:
                return str(int(float(value)))
            except ValueError:
                return value
        return "0"
    except Exception as e:
        print(f"Error in process_price: {e}")
        return "0"

def process_text(input_text, country_tariffs=None):
    """Extract details from input text using AWS Bedrock."""
    try:
        system_msg = (
            "You are an information extraction assistant for industrial procurement. "
            "Read the provided text and extract the following as JSON:\n"
            "{\n"
            '  "Raw_Material": string,\n'
            '  "Vendor_Name": string,\n'
            '  "Price_per_Unit": number or list of numbers,\n'
            '  "Currency": string,\n'
            '  "Country_of_Origin": array of strings\n'
            "}\n"
            "Ensure the response is valid JSON with these exact keys. "
            "Do not include markdown code fences."
        )
        raw_response = invoke_bedrock_text(system_msg, input_text, temperature=0.2, max_tokens=1500)
        print(f"[DEBUG] Bedrock raw response: {raw_response[:500]}...")  # Print first 500 chars
        if not raw_response:
            return {"error": "Empty response from Bedrock"}

        try:
            details = json.loads(raw_response)
            print(f"[DEBUG] Parsed Bedrock details: {details}")
        except json.JSONDecodeError:
            # Attempt to extract JSON if wrapped in text
            json_pattern = r"\{.*\}"
            match = re.search(json_pattern, raw_response, re.DOTALL)
            if not match:
                return {"error": "No JSON data found in the Bedrock response"}
            details = json.loads(match.group(0))
            print(f"[DEBUG] Parsed Bedrock details (extracted): {details}")

        countries = details.get("Country_of_Origin", [])
        if isinstance(countries, str):
            countries = [countries]

        country_tariffs = country_tariffs or {}
        applicable_tariff = 0.0
        for country in countries:
            if not isinstance(country, str):
                continue
            lookup = country.strip().lower()
            if lookup in country_tariffs:
                applicable_tariff = max(applicable_tariff, country_tariffs[lookup] / 100.0)

        raw_material = details.get("Raw_Material", "")

        # Parse pricing data into a numeric list when possible
        pricing_data = details.get("Price_per_Unit", [])
        if pricing_data is None:
            pricing_data = []

        raw_price_entries = []
        if isinstance(pricing_data, list):
            raw_price_entries = pricing_data
        elif pricing_data != "":
            raw_price_entries = [pricing_data]

        parsed_prices = []
        for entry in raw_price_entries:
            if isinstance(entry, (int, float)):
                parsed_prices.append(float(entry))
            elif isinstance(entry, str):
                if is_float(entry):
                    parsed_prices.append(float(entry))
                else:
                    # Attempt to extract numbers embedded in the string
                    matches = re.findall(r"[-+]?\d+(?:\.\d+)?", entry.replace(",", ""))
                    parsed_prices.extend(float(m) for m in matches if is_float(m))

        price_details = search_material_price(raw_material) if raw_material else ""
        market_price = process_price(price_details) if price_details else "0"

        # Apply tariff to parsed supplier prices
        if applicable_tariff and parsed_prices:
            parsed_prices = [round(val * (1 + applicable_tariff), 2) for val in parsed_prices]

        pricing_value = min(parsed_prices) if parsed_prices else None

        # Apply tariff to market price if available
        adjusted_market_price = market_price
        if applicable_tariff and market_price and is_float(market_price):
            numeric_price = round(float(market_price) * (1 + applicable_tariff), 2)
            adjusted_market_price = (
                str(int(numeric_price)) if numeric_price.is_integer() else f"{numeric_price:.2f}"
            )

        # Determine final pricing string
        if pricing_value is not None:
            pricing_str = (
                str(int(pricing_value))
                if float(pricing_value).is_integer()
                else f"{pricing_value:.2f}"
            )
        else:
            pricing_str = adjusted_market_price

        # Optional: keep list of parsed prices for reference
        pricing_breakdown = [
            int(val) if float(val).is_integer() else round(val, 2) for val in parsed_prices
        ]

        result = {
            "country_of_origin": countries,
            "pricing": pricing_str,
            "pricing_breakdown": pricing_breakdown,
            "raw_material": raw_material,
            "vendor_name": details.get("Vendor_Name", ""),
            "currency": details.get("Currency", ""),
            "price": adjusted_market_price,
            "tariff_applied": bool(applicable_tariff),
            "tariff_percentage": round(applicable_tariff * 100, 2) if applicable_tariff else 0.0
        }
        print(f"[DEBUG] process_text result: {json.dumps(result, indent=2)}")
        return result

    except Exception as e:
        print(f"Error in process_text: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

def is_float(element):
    """Check if element can be converted to float."""
    try:
        float(element)
        return True
    except ValueError:
        return False

def analyze_quotes(processed_files):
    """Analyze multiple quotes and provide recommendations."""
    if not processed_files:
        return None
    
    # Find the lowest price
    prices = []
    for quote in processed_files:
        pricing = quote.get('pricing')
        if pricing is None:
            prices.append(float('inf'))
        elif isinstance(pricing, (int, float)):
            prices.append(float(pricing))
        elif isinstance(pricing, str):
            try:
                prices.append(float(pricing))
            except ValueError:
                prices.append(float('inf'))
        elif isinstance(pricing, list):
            try:
                valid_numbers = [float(num) for num in pricing if isinstance(num, (int, float, str)) and is_float(num)]
                if valid_numbers:
                    prices.append(min(valid_numbers))
                else:
                    prices.append(float('inf'))
            except ValueError:
                prices.append(float('inf'))
        else:
            prices.append(float('inf'))

    min_price = min(prices)
    best_price_index = prices.index(min_price)
    
    # Compare prices and create analysis
    analysis = {
        'best_choice': processed_files[best_price_index],
        'price_comparison': [],
        'recommendation': ''
    }
    
    # Calculate price differences
    for i, quote in enumerate(processed_files):
        pricing = quote.get('pricing', 0)
        if isinstance(pricing, list):
            price_list = [float(p) for p in pricing if is_float(p)]
            price = min(price_list) if price_list else 0
        elif pricing is None:
            price = 0
        else:
            price = float(quote.get('pricing', 0))
        
        difference = ((price - min_price) / min_price) * 100 if min_price > 0 else 0
        analysis['price_comparison'].append({
            'vendor': quote.get('vendor_name'),
            'price': price,
            'difference_percentage': round(difference, 2)
        })
    
    # Generate recommendation
    best_vendor = processed_files[best_price_index].get('vendor_name')
    best_price = processed_files[best_price_index].get('price')
    raw_material = processed_files[best_price_index].get('raw_material')
    
    analysis['recommendation'] = f"Based on the price comparison, {best_vendor} offers the best value for {raw_material} at ${best_price}. "
    
    # Add additional insights
    if len(processed_files) > 1:
        second_best = sorted(analysis['price_comparison'], key=lambda x: x['price'])[1]
        price_difference = second_best['difference_percentage']
        analysis['recommendation'] += f"This is {price_difference}% lower than the next best option from {second_best['vendor']}."
    
    return analysis

def extract_text_from_pdf(pdf_data):
    """Extract text from PDF binary data."""
    try:
        pdf_file = BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        full_text = "".join([page.extract_text() for page in pdf_reader.pages])
        return full_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def lambda_handler(event=None, context=None):
    """
    Lambda handler for processing a batch of PDF files from S3 and updating DB rows using rowid from S3 metadata.
    """
    print(f"Lambda handler invoked: event={event}")
    try:
        if not event or 'body' not in event:
            return {
                'statusCode': 400, 
                'body': json.dumps({'error': 'No body in event'})
            }
        payload = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        batch_id = payload.get('batch_id')
        user_id = payload.get('user_id', 1)  # Default user_id if not provided
        
        if not batch_id:
            return {
                'statusCode': 400, 
                'body': json.dumps({'error': 'No batch_id provided'})
            }
        print(f"Received batch_id: {batch_id}, user_id: {user_id}")
        
        db_manager = DatabaseManager()
        country_tariffs = db_manager.fetch_country_tariffs()
        
        # Retrieve all pdf_keys for the batch_id using new method
        rows = db_manager.get_quotations_by_batch_id(batch_id)
        pdf_keys = [row.get('pdf_key') for row in rows if row.get('pdf_key')]
        
        print(f"Found {len(pdf_keys)} PDF keys for batch_id {batch_id}")
        if not pdf_keys:
            return {
                'statusCode': 404, 
                'body': json.dumps({'error': 'No PDF files found for this batch_id'})
            }
        
        s3 = boto3.client('s3')
        bucket_name = os.environ.get('PRIVATE_FILES_BUCKET', 'private-bucket-fastapi')
        processed_data = []
        
        for row in rows:
            key = row.get('pdf_key')
            row_id = row.get('id')
            
            if not key:
                continue
                
            try:
                print(f"Downloading {key} from S3 bucket {bucket_name}")
                s3_obj = s3.get_object(Bucket=bucket_name, Key=key)
                pdf_bytes = s3_obj['Body'].read()
                
                text = extract_text_from_pdf(pdf_bytes)
                print(f"[DEBUG] Extracted text length from {key}: {len(text)} characters")
                print(f"[DEBUG] First 500 chars of extracted text: {text[:500]}...")
                if text:
                    result = process_text(text, country_tariffs)
                    if not isinstance(result, dict) or 'error' not in result:
                        processed_data.append(result)
                        
                        # Update the DB row using row_id
                        if row_id:
                            update_data = {
                                'material_code': result.get('raw_material', ''),
                                'vendor_name': result.get('vendor_name', ''),
                                'price_per_unit': result.get('pricing', 0),
                                'currency': result.get('currency', ''),
                                'country_of_origin': ", ".join(result.get('country_of_origin', []))
                            }
                            print(f"[DEBUG] Updating DB row {row_id} with data: {update_data}")
                            db_manager.update_quotation_by_id(
                                row_id,
                                material_code=update_data['material_code'],
                                vendor_name=update_data['vendor_name'],
                                price_per_unit=update_data['price_per_unit'],
                                currency=update_data['currency'],
                                country_of_origin=update_data['country_of_origin']
                            )
                            print(f"Successfully processed and updated DB for PDF {key} (id={row_id})")
                        else:
                            print(f"[WARNING] No row id found for PDF {key}")
                    else:
                        print(f"Error processing PDF {key}: {result.get('error')}")
                else:
                    print(f"No text extracted from PDF {key}")
            except Exception as e:
                print(f"Error processing PDF {key}: {e}")
                import traceback
                print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                continue
        
        if not processed_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No valid quote data extracted from PDFs'})
            }
        
        analysis = analyze_quotes(processed_data)
        print("Quote analysis completed")
        result = {
            'statusCode': 200, 
            'body': json.dumps({
                'message': f'Successfully processed {len(processed_data)} out of {len(pdf_keys)} PDF files',
                'processed_count': len(processed_data),
                'total_files': len(pdf_keys),
                'processed_data': processed_data,
                'analysis': analysis,
                'batch_id': batch_id
            }, indent=2)
        }
        print(f"\n[RESULT] Final lambda_handler result:\n{json.dumps(json.loads(result['body']), indent=2)}")
        return result
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500, 
            'body': json.dumps({'error': f'Lambda execution failed: {e}'})
        }



if __name__ == "__main__":
    result = lambda_handler({
        "body": json.dumps({
            "batch_id": "afc7c9bb-4898-4b6e-8bff-ffe3503daff2",
    "files": [
        {
            "id": 23,
            "pdfKey": "quoteCompare/ddfe0dac-1588-4f30-be49-8111f3907595.pdf"
        },
        {
            "id": 24,
            "pdfKey": "quoteCompare/1780363e-50b3-4b58-9a29-7d94565840e2.pdf"
        }
    ]
        })
        
    }, None)
    print(f"\n{'='*80}")
    print("FINAL RESULT:")
    print(f"{'='*80}")
    print(json.dumps(result, indent=2, default=str))