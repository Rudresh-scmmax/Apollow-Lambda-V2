import json
import pandas as pd
from datetime import datetime

# Your data
data = {
    "message": "Query executed successfully",
    "rows": [
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-02-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1409.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "7d5d176ef4c0c288c2d341da015d7d75f9df0dfdd7d6005fd0882108a0e8f4cc"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-05-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1375.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "218f786b904107ef3be48e3c124d61e16e604f02f6fa9fb3b77535dd7068757d"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-06-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1205.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "a9d9131b7af14bf217d93059d12cd7a61b000246ced7e725adf9a294a2c5c6c9"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-07-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1250.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "a77b2a2271c762115d1d64e9fee3888ac306a67c33c8b922057af821e55f93de"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-11-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1006.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "e7520bb24e6d55d7e543d175cec960e7022f9fa9a6809b2a050ff62023902125"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2023-12-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "960.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "71f08e17e56bdb6ef2321885f8a75a201a4149397c990911db674931f79f5f84"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-02-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1034.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "6e39ec000db57b77a55188812f0ffda232d86a63dd4f89a25f8c35393bc7e9ea"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-03-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1023.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "511d42705f246c0af36d9a3b09cec9e14009db634fe6b414923106215a0e9565"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-04-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1038.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "82074b12f95300c3706879c3007ed8f318e4cec69f8f6ecb537375786f68c81c"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-05-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1114.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "7e53b204da969a8abd6eb4d6742583585e522d2f056aa3f8cf7761ae0c6d32ed"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-06-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1057.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "a06fff16ebdeb819f4a32ae079c5bc5fbef69ff0b219f9da192e3df9d957cada"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-07-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1090.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "898fac8d5d08af8a54ef29769d6db1fc1255a83a4a6af31d5be3e1a07f674b5e"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2024-09-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "1020.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "0dfba882efaeaeb27e703590c8b62a90c7d6ba06f234d07f430da67671e6d0f7"
        },
        {
            "plant_code": "Plant1",
            "location_desc": None,
            "po_number": "21135661",
            "po_date": "2025-01-01T00:00:00.000Z",
            "buyer_name": "Sukumar, Mr. Shetty",
            "supplier_id": "12813",
            "supplier_name": "BASF India Ltd",
            "supplier_site": "MUMBAI-194Q",
            "material_code": "101834-000000",
            "item_description": "2-Ethylhexanoic Acid",
            "quantity": "59200.0000",
            "uom": "KILOGRAMS",
            "currency": "INR",
            "exchange_rate": "1.0000",
            "price": "926.0000",
            "payment_term": "60 Days Credit from Invoice Date",
            "base_price_fc": "9472000.0000",
            "freight_terms_dsp": "To Sellers A/c",
            "ship_via_lookup_code": "Sea",
            "fob_dsp": "CIF-Mundra",
            "row_hash": "e25ce0c225a21d9425623f3a6f12463423bc7f921d91c01add7d0e57c598ba35"
        }
    ]
}
# Transform the data to match your required CSV structure
transformed_data = []

# Fixed values as per your requirement
FIXED_PURCHASING_ORG_ID = 1
FIXED_PLANT_ID = 1
FIXED_SUPPLIER_ID = "10006"

for row in data['rows']:
    # Get material_code from row and skip if None or empty
    material_code = row.get('material_code')
    if not material_code or material_code is None:
        print(f"Skipping record with PO number {row.get('po_number', 'Unknown')} - no material_code")
        continue
    
    # Calculate total cost (quantity * price)
    try:
        quantity = float(row.get('quantity', '0.0'))
        price = float(row.get('price', '0.0'))
        total_cost = quantity * price
    except (ValueError, TypeError):
        total_cost = 0.0
    
    # Parse date
    try:
        po_date = datetime.fromisoformat(row['po_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d') if row.get('po_date') else ''
    except:
        po_date = row.get('po_date', '')
    
    # Clean buyer name (remove "Mr." and format)
    buyer_name = row.get('buyer_name', '').replace('Mr. ', '').replace(', ', ' ')
    # Use material_code from th
    # e row
    material_id = material_code
    # Normalize UOM to "Kilograms"
    uom = "Kilograms" if row.get('uom') in ['KG', 'KILOGRAMS'] else row.get('uom', '')
    
    transformed_row = {
        'purchasing_org_id': FIXED_PURCHASING_ORG_ID,
        'buyer_name': buyer_name,
        'material_id': material_id,
        'plant_id': FIXED_PLANT_ID,
        'supplier_id': FIXED_SUPPLIER_ID,
        'po_number': row.get('po_number', ''),
        'purchase_date': po_date,
        'currency_of_po': row.get('currency', ''),
        'uom': uom,
        'quantity': int(float(row.get('quantity', '0.0'))) if row.get('quantity', '0.0') != '0.0000' else 0,
        'cost_per_uom': round(float(row.get('price', '0.0')), 2),
        'total_cost': int(total_cost),
        'payment_terms': row.get('payment_term', ''),
        'freight_terms': row.get('freight_terms_dsp', ''),
        'transaction_posting_date': po_date
    }
    
    transformed_data.append(transformed_row)

# Create DataFrame
df = pd.DataFrame(transformed_data)

# Define the column order as specified
column_order = [
    'purchasing_org_id',
    'buyer_name',
    'material_id',
    'plant_id',
    'supplier_id',
    'po_number',
    'purchase_date',
    'currency_of_po',
    'uom',
    'quantity',
    'cost_per_uom',
    'total_cost',
    'payment_terms',
    'freight_terms',
    'transaction_posting_date'
]

df = df[column_order]

# Save to CSV
output_file = 'purchase_orders.csv'
df.to_csv(output_file, index=False)

print(f"CSV file created successfully: {output_file}")
print(f"Total rows: {len(df)}")
print("\nFirst few rows:")
print(df.head())

# Also create Excel version
excel_file = 'purchase_orders.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')
print(f"Excel file also created: {excel_file}")

