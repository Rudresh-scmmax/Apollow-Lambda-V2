import csv
import json
import requests
from fuzzywuzzy import fuzz, process
from db_query import database_query

def get_material_master_data():
    """Query material master data to get material_id and material_description"""
    query = "SELECT material_id, material_description FROM material_master"
    print(f"Executing query: {query}")
    result = database_query(query)
    print(f"Database query result type: {type(result)}")
    print(f"Database query result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    # If the result is a string, try to parse it as JSON
    if isinstance(result, str):
        try:
            result = json.loads(result)
            print(f"Successfully parsed JSON result")
        except json.JSONDecodeError as e:
            print(f"Failed to parse result as JSON: {e}")
            return None
    
    # Check if result has the expected structure
    if result and isinstance(result, dict):
        if 'rows' in result:
            print(f"Found {len(result['rows'])} material master records")
            return result
        elif 'data' in result:
            print(f"Found {len(result['data'])} material master records (data format)")
            return {'rows': result['data']}
        elif 'body' in result:
            # Handle Lambda response format with statusCode and body
            try:
                body_data = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
                if 'rows' in body_data:
                    print(f"Found {len(body_data['rows'])} material master records in body")
                    return body_data
                elif isinstance(body_data, list):
                    print(f"Found {len(body_data)} material master records in body (list format)")
                    return {'rows': body_data}
                else:
                    print(f"Body structure: {list(body_data.keys()) if isinstance(body_data, dict) else type(body_data)}")
                    return None
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing body: {e}")
                return None
        else:
            print(f"Unexpected dict structure: {list(result.keys())}")
            # Try to find any list-like structure
            for key, value in result.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"Found list in key '{key}' with {len(value)} items")
                    return {'rows': value}
            return None
    elif result and isinstance(result, list):
        print(f"Found {len(result)} material master records (list format)")
        return {'rows': result}
    else:
        print("No material master data available. Cannot proceed without material IDs.")
        return None

def get_price_history_data():
    """Query price history data from the API"""
    url = 'https://fucqmp6epk.execute-api.us-east-1.amazonaws.com/api/v1/core/query'
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "sql": "SELECT mm.material_description, mph.price_per_uom, mph.date_month FROM material_price_history mph JOIN master_materials mm ON mm.material_code = mph.material_code WHERE mph.price_per_uom IS NOT NULL ORDER BY mph.date_month;"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying price history API: {e}")
        return None

def match_materials_with_descriptions(price_data, material_master_data):
    """Match material descriptions from API with material master data using fuzzy matching"""
    print(f"Material master data: {material_master_data}")
    print(f"Price data: {price_data}")
    
    # Create a mapping from material_description to material_id
    description_to_id_map = {}
    if material_master_data and 'rows' in material_master_data:
        for row in material_master_data['rows']:
            description_to_id_map[row['material_description']] = row['material_id']
        print(f"Created mapping for {len(description_to_id_map)} materials")
    else:
        print("No material master data available. Cannot proceed without material IDs.")
        return []
    
    # Get all material descriptions from master data for fuzzy matching
    master_descriptions = list(description_to_id_map.keys())
    
    # Process price data and match by description using fuzzy matching
    matched_data = []
    if price_data and 'rows' in price_data:
        print(f"Processing {len(price_data['rows'])} price records")
        for row in price_data['rows']:
            # The API query returns material_description
            material_description = row.get('material_description', '')
            
            # Try exact match first
            material_id = description_to_id_map.get(material_description)
            
            if not material_id:
                # Use fuzzy matching to find the best match
                best_match = process.extractOne(
                    material_description, 
                    master_descriptions, 
                    scorer=fuzz.ratio,
                    score_cutoff=80  # Minimum 80% similarity
                )
                
                if best_match:
                    matched_description, score = best_match
                    material_id = description_to_id_map[matched_description]
                    print(f"Fuzzy matched: '{material_description}' -> '{matched_description}' (score: {score})")
                else:
                    print(f"No good match found for: {material_description}")
                    continue
            else:
                print(f"Exact match: {material_id} - {material_description}")
            
            matched_row = {
                'material_id': material_id,  # Use material_id from material_master table
                'material_description': material_description,
                'price_per_uom': row.get('price_per_uom'),
                'date_month': row.get('date_month'),
                'currency': 'USD'  # All currency as USD as requested
            }
            matched_data.append(matched_row)
    
    return matched_data

# Get data from both sources
print("Fetching material master data...")
material_master_data = get_material_master_data()
print(f"Material master data received: {material_master_data}")

print("Fetching price history data...")
price_data = get_price_history_data()

if not price_data:
    print("Failed to fetch price history data. Using sample data...")
    # Fallback to sample data if API fails
    price_data = {
        "message": "Query executed successfully",
        "rows": [
            {
                "material_description": "Sample Material 1",
                "price_per_uom": "707.5",
                "date_month": "2025-01-31"
            },
            {
                "material_description": "Sample Material 2", 
                "price_per_uom": "369.12",
                "date_month": "2024-10-01"
            }
        ]
    }

# Match materials with descriptions
print("Matching materials with descriptions...")
matched_data = match_materials_with_descriptions(price_data, material_master_data)

if not matched_data:
    print("No matched data found. Please check your data sources.")
    exit(1)

print(f"Found {len(matched_data)} matched records")

# Generate CSV file
print("Generating CSV file...")
with open("price_history_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "material_price_type_period_id", "material_id", "period_start_date", "period_end_date",
        "country", "price", "price_currency", "price_history_source", "price_type", "location_id"
    ])

    for i, row in enumerate(matched_data, start=1):
        # Format date properly
        date_str = row.get("date_month", "")
        if " " in date_str:
            date_str = date_str.split(" ")[0]
        
        writer.writerow([
            f"MPTP{i:04d}",                    # Primary key
            row["material_id"],                # material_id from material_master table
            date_str,                          # period_start_date
            date_str,                          # period_end_date
            "",                                # country (empty)
            row["price_per_uom"],              # price
            "USD",                             # price_currency (all USD as requested)
            "External Source",                 # price_history_source
            "Standard",                        # price_type
            212                                # location_id
        ])

print("✅ CSV file 'price_history_data.csv' generated successfully!")
print(f"Processed {len(matched_data)} records")