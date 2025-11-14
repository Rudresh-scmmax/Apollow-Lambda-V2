from db_query import database_query
import json

"""
Note: For best fuzzy matching results, enable the pg_trgm extension in PostgreSQL:
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    
This script will work without it using pattern matching as a fallback.
"""


def parse_db_result(result):
    """Parse database query result"""
    if isinstance(result, dict):
        if 'body' in result:
            body = result['body']
            if isinstance(body, str):
                try:
                    return json.loads(body)
                except json.JSONDecodeError:
                    return body
            return body
        return result
    elif isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    return result


def find_supplier_id_fuzzy(supplier_name, similarity_threshold=0.3):
    """
    Find supplier_id using fuzzy search with PostgreSQL similarity.
    Uses pg_trgm extension for trigram similarity matching.
    Falls back to pattern matching if pg_trgm is not available.
    """
    # First try exact match (case-insensitive)
    query = """
        SELECT supplier_id, supplier_name 
        FROM supplier_master 
        WHERE LOWER(TRIM(supplier_name)) = LOWER(TRIM(%s))
        LIMIT 1
    """
    result = database_query(query, [supplier_name])
    parsed = parse_db_result(result)
    
    if parsed and isinstance(parsed, list) and len(parsed) > 0:
        return parsed[0].get('supplier_id'), parsed[0].get('supplier_name')
    
    # If no exact match, try fuzzy search using similarity (requires pg_trgm extension)
    try:
        query = """
            SELECT supplier_id, supplier_name,
                   similarity(LOWER(TRIM(supplier_name)), LOWER(TRIM(%s))) as sim_score
            FROM supplier_master 
            WHERE similarity(LOWER(TRIM(supplier_name)), LOWER(TRIM(%s))) > %s
            ORDER BY sim_score DESC
            LIMIT 1
        """
        result = database_query(query, [supplier_name, supplier_name, similarity_threshold])
        parsed = parse_db_result(result)
        
        if parsed and isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0].get('supplier_id'), parsed[0].get('supplier_name')
    except Exception as e:
        print(f"  [INFO] pg_trgm similarity not available, trying pattern matching: {e}")
    
    # Fallback: Try pattern matching using ILIKE with key words
    # Extract key words from supplier name (remove common suffixes and words)
    key_words = supplier_name.upper().replace('.', '').replace(',', '').split()
    # Remove common words
    common_words = {'LTD', 'LIMITED', 'PVT', 'PRIVATE', 'PT', 'PTE', 'SDN', 'BHD', 
                   'CO', 'COMPANY', 'INC', 'INCORPORATED', 'GMBH', 'KG', 'LLC'}
    key_words = [w for w in key_words if w not in common_words and len(w) > 2]
    
    if key_words:
        # Try to find supplier with at least 2 key words matching
        pattern = '%' + '%'.join(key_words[:3]) + '%'  # Use first 3 key words
        query = """
            SELECT supplier_id, supplier_name
            FROM supplier_master 
            WHERE UPPER(supplier_name) LIKE %s
            ORDER BY 
                CASE WHEN LOWER(TRIM(supplier_name)) LIKE LOWER(%s) THEN 1 ELSE 2 END,
                LENGTH(supplier_name)
            LIMIT 1
        """
        result = database_query(query, [pattern, f"%{supplier_name}%"])
        parsed = parse_db_result(result)
        
        if parsed and isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0].get('supplier_id'), parsed[0].get('supplier_name')
    
    return None, None


def insert_vendor_key_info(supplier_id, supplier_site, material_id, capacity, 
                           capacity_expansion_plans, fta_benefit, remarks):
    """Insert or update vendor key information"""
    # Convert empty strings to None for NULL values
    capacity = None if capacity == "" else capacity
    capacity_expansion_plans = None if capacity_expansion_plans == "" else capacity_expansion_plans
    fta_benefit = None if fta_benefit == "" else fta_benefit
    remarks = None if remarks == "" else remarks
    
    # Convert capacity to numeric if it's a string
    if capacity is not None and isinstance(capacity, str):
        try:
            capacity = float(capacity)
        except ValueError:
            capacity = None
    
    query = """
        INSERT INTO vendor_key_information 
        (supplier_id, supplier_site, material_id, capacity, capacity_expansion_plans, fta_benefit, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
    """
    
    # Note: If you want to update on conflict, use:
    # ON CONFLICT (supplier_id, material_id, supplier_site) 
    # DO UPDATE SET capacity = EXCLUDED.capacity, ...
    
    result = database_query(query, [
        supplier_id, supplier_site, material_id, capacity,
        capacity_expansion_plans, fta_benefit, remarks
    ])
    
    return parse_db_result(result)


data = [
        {
            "id": 128,
            "supplier_name": "Adani Wilmar Ltd.",
            "supplier_site": "AHMEDABAD",
            "material_code": "100724-000000",
            "capacity": "",
            "capacity_expansion_plans": "",
            "fta_benefit": "",
            "remarks": "",
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-11-13T11:56:02.505Z"
        },
        {
            "id": 114,
            "supplier_name": "SHEEL OIL AND FATS PVT. LTD.",
            "supplier_site": "KUTCH-194Q",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 115,
            "supplier_name": "MANUCHAR HONG KONG LIMITED",
            "supplier_site": "HONG KONG",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 122,
            "supplier_name": "Godrej Industries Ltd",
            "supplier_site": "MUMBAI",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 123,
            "supplier_name": "RUCHI SOYA INDUSTRIES LTD",
            "supplier_site": "GANDHIDHAM-194Q",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 124,
            "supplier_name": "Inter-Continental Oils and Fats Pte. Ltd.",
            "supplier_site": "SINGAPORE",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 133,
            "supplier_name": "WILMAR TRADING PTE LTD",
            "supplier_site": "SINGAPORE",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 138,
            "supplier_name": "JPN ASIA PTE LTD",
            "supplier_site": "Singapore",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 148,
            "supplier_name": "AMBER CHEMICALS",
            "supplier_site": "Mumbai-194Q",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 149,
            "supplier_name": "Sheel Chand Agroils (P) ltd",
            "supplier_site": "RUDRAPUR",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 151,
            "supplier_name": "OZONE POLYFORM PVT. LTD",
            "supplier_site": "Mumbai-194Q",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 157,
            "supplier_name": "VVF (India) Limited",
            "supplier_site": "MUMBAI",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 158,
            "supplier_name": "Natural Oleochemicals Sdn. Bhd.",
            "supplier_site": "MALAYSIA",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 159,
            "supplier_name": "THAI OLEOCHEMICALS CO. LTD.",
            "supplier_site": "THAILAND",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 160,
            "supplier_name": "Shreeshyam Oleo Chemicals Pvt Ltd",
            "supplier_site": "Medinipur-194Q",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 174,
            "supplier_name": "Global Green Chemicals Public Company Limited",
            "supplier_site": "CHATUCHAK",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 176,
            "supplier_name": "PT. SINARMAS BIO ENERGY",
            "supplier_site": "JAKARTA",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 177,
            "supplier_name": "CREMER OLEO GmbH & Co. KG",
            "supplier_site": "HAMBURG",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 181,
            "supplier_name": "PT DUA KUDA INDONESIA",
            "supplier_site": "JAKARTA UTARA",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 191,
            "supplier_name": "PT. BINA KARYA PRIMA",
            "supplier_site": "JAKARTA",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 192,
            "supplier_name": "PT SOCI MAS",
            "supplier_site": "DELI SERDANG, N",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 203,
            "supplier_name": "WILMAR INTERNATIONAL LIMITED",
            "supplier_site": "SINGAPORE",
            "material_code": "100724-000000",
            "capacity": None,
            "capacity_expansion_plans": None,
            "fta_benefit": None,
            "remarks": None,
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-08T17:06:45.902Z"
        },
        {
            "id": 172,
            "supplier_name": "APICAL (MALAYSIA) SDN. BHD.",
            "supplier_site": "Malaysia",
            "material_code": "100724-000000",
            "capacity": "0.24",
            "capacity_expansion_plans": "",
            "fta_benefit": "ASEAN ",
            "remarks": "",
            "created_at": "2025-07-08T17:06:45.902Z",
            "updated_at": "2025-07-20T13:19:09.392Z"
        }
    ]


# Process each record
success_count = 0
failed_count = 0
not_found_count = 0

for d in data:
    supplier_name = d['supplier_name']
    material_code = d['material_code']
    
    print(f"\nProcessing: {supplier_name}")
    
    # Find supplier_id using fuzzy search
    supplier_id, matched_name = find_supplier_id_fuzzy(supplier_name, similarity_threshold=0.3)
    
    if supplier_id:
        print(f"  ✓ Found supplier_id: {supplier_id} (matched: {matched_name})")
        
        # Insert into vendor_key_information table
        try:
            result = insert_vendor_key_info(
                supplier_id=supplier_id,
                supplier_site=d.get('supplier_site'),
                material_id=material_code,
                capacity=d.get('capacity'),
                capacity_expansion_plans=d.get('capacity_expansion_plans'),
                fta_benefit=d.get('fta_benefit'),
                remarks=d.get('remarks')
            )
            
            if result:
                print(f"  ✓ Inserted into vendor_key_information")
                success_count += 1
            else:
                print(f"  ⚠ Insert returned no result (may already exist)")
                success_count += 1
                
        except Exception as e:
            print(f"  ✗ Error inserting: {e}")
            failed_count += 1
    else:
        print(f"  ✗ Supplier not found: {supplier_name}")
        not_found_count += 1

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Successfully processed: {success_count}")
print(f"  Failed: {failed_count}")
print(f"  Not found: {not_found_count}")
print(f"{'='*60}")