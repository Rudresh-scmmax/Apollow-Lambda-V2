import json
import boto3


def database_query(query, params=None):
    client = boto3.client("lambda")
    Payload = json.dumps({"query": query, "params": params or []})
    
    try:
        resp = client.invoke(
            FunctionName="private_db_query",
            InvocationType="RequestResponse",
            Payload=Payload
        )
        
        # Read the payload
        payload = resp["Payload"].read()
        result = json.loads(payload)
        return result
        
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Lambda invocation failed: {str(e)}"
        }