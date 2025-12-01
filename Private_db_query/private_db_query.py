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
            
            # Check if query returns results (SELECT or queries with RETURNING clause)
            # RETURNING clause can appear in INSERT, UPDATE, DELETE statements
            query_upper = query.strip().upper()
            has_returning = "RETURNING" in query_upper
            is_select = query_upper.startswith("SELECT")
            
            # If it's a SELECT or has RETURNING clause, fetch results
            if is_select or has_returning:
                # Check if cursor has description (i.e., returns rows)
                if cur.description is not None and len(cur.description) > 0:
                    try:
                        # Fetch all rows - this should work even for large result sets
                        rows = cur.fetchall()
                        row_count = len(rows) if rows else 0
                        
                        # IMPORTANT: For INSERT/UPDATE/DELETE with RETURNING, commit BEFORE processing results
                        # This ensures that if there's a parsing error, the data is already committed
                        if not is_select:
                            conn.commit()
                        
                        # Safely extract column names
                        colnames = []
                        for idx, desc in enumerate(cur.description):
                            try:
                                # psycopg2 description is a tuple: (name, type_code, display_size, internal_size, precision, scale, null_ok)
                                # First element is the column name
                                if desc and isinstance(desc, (tuple, list)) and len(desc) > 0:
                                    colname = desc[0]
                                    if colname:
                                        colnames.append(colname)
                                    else:
                                        # Empty name, use fallback
                                        colnames.append(f"column_{idx}")
                                else:
                                    # Invalid description format, use fallback
                                    colnames.append(f"column_{idx}")
                            except (IndexError, TypeError, AttributeError) as e:
                                # If accessing desc[0] fails, use fallback
                                colnames.append(f"column_{idx}")
                        
                        # Convert rows to list of dictionaries
                        # For large result sets, this might take time but should complete
                        if colnames:
                            result = [dict(zip(colnames, row)) for row in rows]
                        else:
                            # No column names available, return as list of lists
                            result = [list(row) for row in rows]
                        
                        # Verify we converted all rows
                        if len(result) != row_count:
                            raise ValueError(f"Row count mismatch: fetched {row_count} rows but converted {len(result)}")
                        
                        # For SELECT queries, commit is not needed but won't hurt
                        if is_select:
                            conn.commit()
                        
                        # Return all results - ensure we're returning the full list
                        # The result list should contain all rows that were fetched
                        return {
                            "statusCode": 200,
                            "body": json.dumps(result, default=json_serializer)
                        }
                    except Exception as fetch_error:
                        # If fetching/processing fails AFTER commit, we can't rollback
                        # For INSERT/UPDATE/DELETE, data is already committed, so return partial success
                        # For SELECT, we can safely return error
                        if not is_select:
                            # Data was already committed, so return error but note that data was saved
                            error_msg = str(fetch_error)
                            return {
                                "statusCode": 500,
                                "body": json.dumps({
                                    "error": f"Error processing results (data was committed): {error_msg}",
                                    "data_committed": True
                                }, default=json_serializer)
                            }
                        else:
                            # For SELECT, rollback is safe (no data was changed)
                            conn.rollback()
                            error_msg = str(fetch_error)
                            return {
                                "statusCode": 500,
                                "body": json.dumps({"error": f"Error fetching results: {error_msg}"}, default=json_serializer)
                            }
                else:
                    # No description means no rows returned (shouldn't happen with SELECT/RETURNING, but handle it)
                    # Still commit the transaction for INSERT/UPDATE/DELETE with RETURNING
                    if not is_select:
                        conn.commit()
                    return {
                        "statusCode": 200,
                        "body": json.dumps([], default=json_serializer)
                    }
            
            # For non-SELECT queries without RETURNING (INSERT/UPDATE/DELETE)
            # Commit the transaction
            conn.commit()
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Query executed successfully"}, default=json_serializer)
            }
            
    except Exception as e:
        # Rollback on error
        try:
            conn.rollback()
        except:
            pass  # Ignore rollback errors if connection is already closed
        error_msg = str(e)
        error_type = type(e).__name__
        # Include more context in error for debugging
        import traceback
        error_trace = traceback.format_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": error_msg,
                "error_type": error_type,
                "query_preview": query[:200] if query else "No query"
            }, default=json_serializer)
        }
    finally:
        try:
            conn.close()
        except:
            pass  # Ignore close errors

