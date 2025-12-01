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
        
        body = resp["Payload"].read()
        result = json.loads(body)
        return result
        
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Lambda invocation failed: {str(e)}"
        }