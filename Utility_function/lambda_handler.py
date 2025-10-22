import json
import os
# import cyclical_pattern
# import correlation_value
import porters_analysis
# import negotiation_obj
# import demand_supply_summary

def lambda_handler(event, context):
    print(f"event: {event}")
    """
    AWS Lambda handler for processing requests related to cyclical patterns, correlation values, and negotiation analysis.

    Expected event structure:
    {
        "action": "cyclical_pattern" or "correlation" or "porters_analysis" or "negotiation_avoids" or "demand_supply_summary",
        "material_id": "M036",
        "region": "China - Qingdao"
    }
    or
    {
        "action": "correlation_value",
        "material_ids": ["M037", "M036"]
    }
    or
    {
        "action": "negotiation_avoids",
        "vendor_name": "Supplier Name",
        "date": "2024-01-15",
        "material_id": "M036",
        "region": "Asia-Pacific",
        "force_refresh": false  # Optional: force regeneration even if data exists
    }
    """

    # Parse body if present (API Gateway), else use event directly
    if "body" in event:
        body = json.loads(event.get("body", "{}"))
    else:
        body = event

    action = body.get("action")

    # if action == "cyclical_pattern":
    #     # Cyclical pattern request
    #     try:
    #         material_id = body.get("material_id")
    #         region = body.get("region")

    #         if not material_id or not region:
    #             return {
    #                 "statusCode": 400,
    #                 "headers": {
    #                     "Content-Type": "application/json",
    #                     "Access-Control-Allow-Origin": "*"
    #                 },
    #                 "body": json.dumps({"error": "Missing 'material_id' or 'region' parameter in the request"})
    #             }

    #         # Pass as event dict to match cyclical_pattern.lambda_handler signature
    #         cyclical_event = {
    #             "material_id": material_id,
    #             "region": region
    #         }
    #         result = cyclical_pattern.lambda_handler(cyclical_event, context)
    #         return {
    #             "statusCode": 200,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps(result)
    #         }
    #     except Exception as e:
    #         print("Error generating cyclical pattern:", str(e))
    #         return {
    #             "statusCode": 500,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps({"error": f"Error generating cyclical pattern: {str(e)}"})
    #         }

    # elif action == "correlation":
    #     # Correlation value request
    #     try:
    #         # Accept either a single material_id or a list of material_ids
    #         material_ids = body.get("material_ids")
    #         material_id = body.get("material_id")

    #         if material_ids and isinstance(material_ids, list) and len(material_ids) >= 2:
    #             corr_event = {"material_ids": material_ids}
    #         elif material_id:
    #             corr_event = {"material_ids": [material_id]}
    #         else:
    #             return {
    #                 "statusCode": 400,
    #                 "headers": {
    #                     "Content-Type": "application/json",
    #                     "Access-Control-Allow-Origin": "*"
    #                 },
    #                 "body": json.dumps({"error": "Missing 'material_ids' (array) or 'material_id' parameter in the request"})
    #             }

    #         result = correlation_value.lambda_handler(corr_event, context)
    #         return {
    #             "statusCode": 200,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps(result)
    #         }
    #     except Exception as e:
    #         print("Error generating correlation value:", str(e))
    #         return {
    #             "statusCode": 500,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps({"error": f"Error generating correlation value: {str(e)}"})
    #         }

    if action == "porters_analysis":
        # Porter's Five Forces analysis request
        try:
            material_id = body.get("material_id")
            if not material_id:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"error": "Missing 'material_id' parameter in the request"})
                }
            porters_event = {"material_id": material_id}
            result = porters_analysis.lambda_handler(porters_event, context)
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(result)
            }
        except Exception as e:
            print("Error generating porter's analysis:", str(e))
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": f"Error generating porter's analysis: {str(e)}"})
            } 

    # elif action == "negotiation_avoids":
    #     # Negotiation avoids analysis request
    #     # This is the fire-and-forget handler - it processes and saves to DB
    #     try:
    #         material_id = body.get("material_id")
    #         vendor_name = body.get("vendor_name")
    #         region = body.get("region", "Asia-Pacific")
    #         date = body.get("date")
    #         force_refresh = body.get("force_refresh", False)
            
    #         print(f"🔥 [NEGOTIATION_AVOIDS] Processing for vendor={vendor_name}, material={material_id}, date={date}, force_refresh={force_refresh}")

    #         if not vendor_name or not material_id or not date:
    #             return {
    #                 "statusCode": 400,
    #                 "headers": {
    #                     "Content-Type": "application/json",
    #                     "Access-Control-Allow-Origin": "*"
    #                 },
    #                 "body": json.dumps({
    #                     "error": "Missing required parameters: 'vendor_name', 'material_id', or 'date'"
    #                 })
    #             }

    #         # Pass to negotiation_obj.lambda_handler which handles the full workflow
    #         negotiation_event = {
    #             "vendor_name": vendor_name,
    #             "material_id": material_id,
    #             "region": region,
    #             "date": date,
    #             "force_refresh": force_refresh
    #         }
            
    #         # This function now handles DB operations internally
    #         result = negotiation_obj.lambda_handler(negotiation_event, context)
            
    #         # Check if result is already a proper response dict
    #         if isinstance(result, dict) and "statusCode" in result:
    #             return result
            
    #         # Otherwise wrap it
    #         return {
    #             "statusCode": 200,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps(result) if isinstance(result, dict) else result
    #         }
            
    #     except Exception as e:
    #         print(f"❌ [NEGOTIATION_AVOIDS ERROR] {str(e)}")
    #         import traceback
    #         print(traceback.format_exc())
    #         return {
    #             "statusCode": 500,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps({
    #                 "error": f"Error generating negotiation avoids analysis: {str(e)}",
    #                 "trace": traceback.format_exc()
    #             })
    #         }

    # elif action == "demand_supply_summary":
    #     # Demand and supply summary request
    #     try:
    #         result = demand_supply_summary.lambda_handler(event, context)
    #         return {
    #             "statusCode": 200,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps(result)
    #         }
    #     except Exception as e:
    #         print("Error generating demand and supply summary:", str(e))
    #         return {
    #             "statusCode": 500,
    #             "headers": {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*"
    #             },
    #             "body": json.dumps({"error": f"Error generating demand and supply summary: {str(e)}"})
    #         }
    
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Invalid or missing 'action' parameter",
                "valid_actions": [
                    "cyclical_pattern",
                    "correlation",
                    "porters_analysis",
                    "negotiation_avoids",
                    "demand_supply_summary"
                ]
            })
        }