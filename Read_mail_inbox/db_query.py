import json
import os
import boto3

TARGET_FUNCTION = os.environ.get("PRIVATE_DB_QUERY_FUNCTION", "private_db_query")


def database_query(query, params=None):
    client = boto3.client("lambda")
    payload = json.dumps({"query": query, "params": params or []})
    
    try:
        resp = client.invoke(
            FunctionName=TARGET_FUNCTION,
            InvocationType="RequestResponse",
            Payload=payload
        )
        
        # Read the payload
        raw_payload = resp["Payload"].read()
        result = json.loads(raw_payload)
        
        # Debug: print the result structure
        print(f"[DEBUG] database_query result type: {type(result)}")
        if isinstance(result, dict):
            print(f"[DEBUG] database_query result keys: {result.keys()}")
            if 'statusCode' in result:
                print(f"[DEBUG] database_query statusCode: {result.get('statusCode')}")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Lambda invocation failed: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "error": f"Lambda invocation failed: {str(e)}"
        }