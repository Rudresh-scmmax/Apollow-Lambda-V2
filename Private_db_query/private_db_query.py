import psycopg2
import json
import os
from datetime import date, datetime
from decimal import Decimal

def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=os.environ.get("DB_PORT", 5432)
    )

def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def lambda_handler(event, context):
    query = event["query"]
    params = event.get("params", [])
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if query.strip().lower().startswith("select"):
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                result = [dict(zip(colnames, row)) for row in rows]
                return {"statusCode": 200, "body": json.dumps(result, default=json_serializer)}
        conn.commit()
        return {"statusCode": 200, "body": json.dumps({"message": "Query executed successfully"}, default=json_serializer)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)}, default=json_serializer)}
    finally:
        conn.close()
