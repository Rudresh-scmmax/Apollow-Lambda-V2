import json
import boto3


def database_query(query, params=None):
    client = boto3.client("lambda")
    Payload = json.dumps({"query": query, "params": params or []})
    resp = client.invoke(
        FunctionName="private_db_query",
        InvocationType="RequestResponse",
        Payload=Payload
    )
    result = json.load(resp["Payload"])
    
    # If the result is a string, try to parse it as JSON
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            print(f"Failed to parse result as JSON: {result}")
            return None
    
    return result