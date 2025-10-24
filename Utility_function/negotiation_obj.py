import os
import json
import traceback
import boto3
import time
from datetime import datetime, timedelta
from typing import Dict, Any, TypedDict, List
from db_query import database_query

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END


# ======================
# 🔐 AWS + Bedrock Config
# ======================
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


class ProcurementState(TypedDict):
    """State schema for LangGraph workflow"""
    material_id: str
    vendor_name: str
    location_id: str
    date: str
    report: Dict[str, Any]
    price_analysis: str
    procurement_strategy: str
    negotiation_intelligence: str
    strategic_questions: str
    error: str


# ======================
# 🗄️ Database Helper Functions
# ======================
def test_db_connection():
    """Test database connection and return status"""
    try:
        result = database_query("SELECT 1")
        if isinstance(result, dict) and result.get('statusCode') == 500:
            return {"success": False, "error": result.get('error', 'Database connection failed')}
        return {"success": True, "message": "Database connection successful"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_query(sql: str, params=None) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as list of dictionaries"""
    try:
        result = database_query(sql, params or [])
        
        # Check for errors first
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"⚠️ [SQL ERROR] {result.get('error')}")
            return []
        
        # Handle different response formats
        if isinstance(result, str):
            try:
                body = json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse string result: {result}")
                return []
        elif isinstance(result, dict) and "body" in result:
            try:
                body = json.loads(result["body"])
            except json.JSONDecodeError:
                print(f"Failed to parse body: {result['body']}")
                return []
        else:
            body = result
        
        if not isinstance(body, list):
            print(f"Expected list but got: {type(body)} - {body}")
            return []
        
        return body
    
    except Exception as e:
        print(f"⚠️ [SQL ERROR] {str(e)}")
        print(f"Query: {sql}")
        return []


def check_existing_recommendations(vendor_name: str, date: str, material_id: str) -> Dict[str, Any]:
    """Check if recommendations already exist in database"""
    try:
        query = """
            SELECT strategy, market_update, updated_at
            FROM negotiation_recommendations
            WHERE vendor_name = %s 
              AND month_start = DATE_TRUNC('month', %s::date)::date
              AND material_id = %s
            LIMIT 1;
        """
        
        result = database_query(query, [vendor_name, date, material_id])
        
        # Check for errors first
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"❌ [DB CHECK ERROR] {result.get('error')}")
            return {"exists": False, "error": result.get('error')}
        
        # Handle different response formats
        if isinstance(result, str):
            try:
                body = json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse string result: {result}")
                return {"exists": False}
        elif isinstance(result, dict) and "body" in result:
            try:
                body = json.loads(result["body"])
            except json.JSONDecodeError:
                print(f"Failed to parse body: {result['body']}")
                return {"exists": False}
        else:
            body = result
        
        if body and len(body) > 0:
            row = body[0]
            return {
                "exists": True,
                "strategy": row.get('strategy') or {},
                "market_update": row.get('market_update') or {},
                "updated_at": row.get('updated_at')
            }
        
        return {"exists": False}
    
    except Exception as e:
        print(f"❌ [DB CHECK ERROR] {str(e)}")
        return {"exists": False, "error": str(e)}


def save_recommendations_to_db(vendor_name: str, date: str, material_id: str, 
                                strategy: Dict, market_update: Dict):
    """Save or update recommendations in database"""
    try:
        query = """
            INSERT INTO negotiation_recommendations 
              (vendor_name, date, month_start, strategy, market_update, updated_at, material_id)
            VALUES 
              (%s, %s, DATE_TRUNC('month', %s::date)::date, %s::jsonb, %s::jsonb, CURRENT_TIMESTAMP, %s)
            ON CONFLICT (vendor_name, month_start, material_id)
            DO UPDATE SET 
              strategy = EXCLUDED.strategy,
              market_update = EXCLUDED.market_update,
              updated_at = CURRENT_TIMESTAMP
            RETURNING *;
        """
        
        result = database_query(query, [
            vendor_name, date, date, 
            json.dumps(strategy), 
            json.dumps(market_update), 
            material_id
        ])
        
        # Check for errors
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"❌ [DB SAVE ERROR] {result.get('error')}")
            return {"success": False, "error": result.get('error')}
        
        print(f"✅ [DB SAVE] Successfully saved recommendations for {vendor_name}")
        return {"success": True, "result": result}
    
    except Exception as e:
        print(f"❌ [DB SAVE ERROR] {str(e)}")
        return {"success": False, "error": str(e)}


def get_material_name(material_id: str) -> str:
    """Fetch material description from material_master"""
    try:
        query = """
            SELECT material_description
            FROM material_master
            WHERE material_id = %s
            LIMIT 1;
        """
        
        result = database_query(query, [material_id])
        
        # Check for errors first
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"⚠️ [MATERIAL FETCH ERROR] {result.get('error')}")
            return "Unknown Material"
        
        # Handle different response formats
        if isinstance(result, str):
            try:
                body = json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse string result: {result}")
                return "Unknown Material"
        elif isinstance(result, dict) and "body" in result:
            try:
                body = json.loads(result["body"])
            except json.JSONDecodeError:
                print(f"Failed to parse body: {result['body']}")
                return "Unknown Material"
        else:
            body = result
        
        if body and len(body) > 0 and body[0].get('material_description'):
            return body[0]['material_description']
        
        print(f"⚠️ No material found for ID: {material_id}")
        return "Unknown Material"
    
    except Exception as e:
        print(f"⚠️ [MATERIAL FETCH ERROR] {str(e)}")
        return "Unknown Material"


# ======================
# 🧠 Material Analysis Builder
# ======================
def get_material_analysis(material_id, vendor_name, location_id):
    """Fetch and compile material analysis data"""
    six_months_ago = (datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%d")

    # ---- PRICE HISTORY ----
    price_query = """
        SELECT *
        FROM price_history_data
        WHERE material_id = %s
          AND location_id = %s
          AND price IS NOT NULL
        ORDER BY period_start_date DESC
        LIMIT 6;
    """
    
    try:
        price_data = run_query(price_query, [material_id, location_id])
    except Exception as e:
        print(f"⚠️ [PRICE QUERY ERROR] {str(e)}")
        price_data = []
    
    historical_prices = []
    news_items = []

    for row in price_data:
        price_date = row['period_start_date'] if row['period_start_date'] else "Unknown Date"
        price_value = float(row['price']) if row['price'] else 0
        currency = row.get('price_currency', 'USD')
        historical_prices.append(f"{price_date}: {currency} {price_value:.2f}")

    historical_price_data = " → ".join(historical_prices) if historical_prices else "No recent price data found."
    news_summary = "No recent news found."

    # ---- PORTER'S 5 FORCES ----
    porter_data = []
    porters_summary = "No Porter's analysis available."
    
    try:
        porter_query = """
            SELECT * FROM porters_analysis
            WHERE material_id = %s
            LIMIT 1;
        """
        
        porter_data = run_query(porter_query, [material_id])
        
        if porter_data:
            try:
                p = porter_data[0]["analysis_json"].get("porters_analysis", {})
                porters_summary = f"""
Threat of New Entrants: {p.get('threat_new_entrants', {}).get('description', 'Unknown')}
Buyer Power: {p.get('bargaining_power_buyers', {}).get('description', 'Unknown')}
Supplier Power: {p.get('bargaining_power_suppliers', {}).get('description', 'Unknown')}
Threat of Substitutes: {p.get('threat_of_substitution', {}).get('description', 'Unknown')}
Rivalry Among Existing Competitors: {p.get('competitive_rivalry', {}).get('description', 'Unknown')}
"""
            except Exception as e:
                print(f"⚠️ Porter's analysis parsing error: {e}")
                porters_summary = "No Porter's analysis available."
        
    except Exception as e:
        print(f"⚠️ [PORTER QUERY ERROR] {str(e)} - Table may not exist, continuing without Porter's analysis")
        porters_summary = "No Porter's analysis available."

    # ---- MARKET RESEARCH ----
    takeaway_query = """
        SELECT *
        FROM material_research_reports
        WHERE material_id = %s
        ORDER BY created_at DESC 
        LIMIT 1;
    """
    
    try:
        takeaway_data = run_query(takeaway_query, [material_id])
    except Exception as e:
        print(f"⚠️ [TAKEAWAY QUERY ERROR] {str(e)}")
        takeaway_data = []
    
    market_research = takeaway_data[0].get("takeaway", "No market research available.") if takeaway_data else "No market research available."

    return {
        "material_name": porter_data[0].get("analysis_json", {}).get("material_name", material_id) if porter_data else material_id,
        "vendor_name": vendor_name,
        "location_id": location_id,
        "historical_price_data": historical_price_data,
        "available_inventory": "",
        "news": news_summary,
        "market_research": market_research,
        "porters_five_forces_analysis": porters_summary.strip()
    }


# ======================
# 🧩 LLM Configuration
# ======================
def create_bedrock_llm(temperature=0.7):
    """Initialize Bedrock LLM using ChatBedrock"""
    return ChatBedrock(
        region_name="us-east-1",
        model_id="us.meta.llama4-scout-17b-instruct-v1:0",
        model_kwargs={
            "temperature": temperature,
            "top_p": 0.9,
            "max_tokens": 2048,
        }
    )


# ======================
# 🔄 LangGraph Nodes
# ======================
def price_prediction_node(state: ProcurementState) -> Dict[str, Any]:
    """Node 1: Price Prediction Analysis"""
    print("📊 [PRICE PREDICTOR] Starting commodity price analysis...")
    llm = create_bedrock_llm(0.7)
    
    prompt = f"""You are a senior commodity strategist with 15+ years experience at major trading firms.

Conduct advanced commodity price analysis for {state['report']['material_name']} in the {state['location_id']} region.

MARKET INTELLIGENCE:
- Historical price data: {state['report']['historical_price_data']}
- Recent news: {state['report']['news']}
- Market research: {state['report']['market_research']}

REQUIRED ANALYSIS:
1. Price trend prediction with 90% confidence intervals (next 3, 6, 12 months)
2. Key inflection points and timing windows
3. Supply-demand imbalance analysis
4. Geopolitical and regulatory risk assessment
5. Seasonal/cyclical pattern identification
6. Forward curve analysis vs spot pricing
7. Volatility assessment and hedging implications
8. Vendor-specific market positioning and pricing power

Provide comprehensive market intelligence with specific timing recommendations."""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content if hasattr(response, 'content') else str(response)
        print(f"✅ [PRICE PREDICTOR] Analysis complete")
        return {"price_analysis": result}
    except Exception as e:
        print(f"❌ [PRICE PREDICTOR] Error: {str(e)}")
        return {"price_analysis": f"Error: {str(e)}", "error": str(e)}


def procurement_strategy_node(state: ProcurementState) -> Dict[str, Any]:
    """Node 2: Procurement Strategy (Kraljic Matrix)"""
    print("📋 [PROCUREMENT STRATEGIST] Developing Kraljic-based strategy...")
    llm = create_bedrock_llm(0.7)
    price_summary = state['price_analysis'][:1000] if state['price_analysis'] else "No price analysis available"
    
    prompt = f"""You are a strategic procurement director with deep expertise in the Kraljic Purchasing Portfolio Matrix.

Develop Kraljic-based procurement strategy for {state['report']['material_name']} with vendor {state['vendor_name']}.

INPUT DATA:
- Price Analysis: {price_summary}...
- Porter's Five Forces: {state['report']['porters_five_forces_analysis']}
- Vendor: {state['vendor_name']}

KRALJIC MATRIX ANALYSIS:
1. Classify material into Kraljic quadrant (Strategic/Leverage/Bottleneck/Routine)
2. Assess profit impact
3. Evaluate supply risk
4. Vendor-specific risk assessment

STRATEGY DEVELOPMENT:
- For Strategic items: Focus on partnership, innovation, risk mitigation
- For Leverage items: Maximize competition, aggressive negotiation
- For Bottleneck items: Secure supply, reduce dependency
- For Routine items: Efficiency, automation, consolidation

Provide comprehensive procurement strategy with specific objectives and vendor-specific approach."""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content if hasattr(response, 'content') else str(response)
        print(f"✅ [PROCUREMENT STRATEGIST] Strategy development complete")
        return {"procurement_strategy": result}
    except Exception as e:
        print(f"❌ [PROCUREMENT STRATEGIST] Error: {str(e)}")
        return {"procurement_strategy": f"Error: {str(e)}", "error": str(e)}


def negotiation_intelligence_node(state: ProcurementState) -> Dict[str, Any]:
    """Node 3: Advanced Negotiation Intelligence"""
    print("🎯 [NEGOTIATION ANALYST] Generating negotiation intelligence...")
    llm = create_bedrock_llm(0.6)
    strategy_summary = state['procurement_strategy'][:1000] if state['procurement_strategy'] else "No strategy available"
    
    prompt = f"""You are a master negotiator and former McKinsey procurement consultant.

Generate advanced negotiation intelligence for {state['report']['material_name']} procurement with vendor {state['vendor_name']}.

CONTEXT:
- Procurement Strategy: {strategy_summary}...
- Porter's Analysis: {state['report']['porters_five_forces_analysis']}
- Vendor: {state['vendor_name']}

RESPOND WITH VALID JSON ONLY - NO ADDITIONAL TEXT:

Identify:
1. BUYER RISKS TO AVOID: 4 specific tactical mistakes with references to contract terms, timing, or market dynamics
2. SUPPLIER AVOID: 4 specific supplier fears or pressures with business impact

Include references to:
- Specific contract terms (payment terms, volume commitments, delivery timing)
- Supplier cost structures and margin pressures
- Competitive threats and market dynamics
- Geopolitical factors and tariffs
- {state['vendor_name']}-specific vulnerabilities

JSON Format:
{{
    "buyerAvoid": [
        "mistake 1 with specific reference",
        "mistake 2 with timing reference",
        "mistake 3 with market reference",
        "mistake 4 with cost reference"
    ],
    "supplierAvoid": [
        "fear 1 with business impact",
        "fear 2 with competitive threat",
        "fear 3 with operational risk",
        "fear 4 with relationship risk"
    ]
}}"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content if hasattr(response, 'content') else str(response)
        print(f"✅ [NEGOTIATION ANALYST] Intelligence generation complete")
        return {"negotiation_intelligence": result}
    except Exception as e:
        print(f"❌ [NEGOTIATION ANALYST] Error: {str(e)}")
        return {"negotiation_intelligence": f"Error: {str(e)}", "error": str(e)}


def question_architecture_node(state: ProcurementState) -> Dict[str, Any]:
    """Node 4: Strategic Question Architect"""
    print("❓ [QUESTION ARCHITECT] Designing negotiation questions...")
    llm = create_bedrock_llm(0.7)
    intel_summary = state['negotiation_intelligence'][:1000] if state['negotiation_intelligence'] else "No intelligence available"
    
    prompt = f"""You are an elite negotiation coach trained at Harvard's Program on Negotiation.

Design the 5 MOST IMPORTANT negotiation questions for {state['report']['material_name']} vendor meetings with {state['vendor_name']}.

INTELLIGENCE INPUTS:
- Negotiation Intelligence: {intel_summary}...
- Vendor: {state['vendor_name']}
- Location: {state['location_id']}

SELECT 5 CRITICAL QUESTIONS ONLY - Focus on highest-impact questions:

1. ONE MARKET INTELLIGENCE PROBE:
   - Test {state['vendor_name']}'s market knowledge and competitive positioning

2. ONE CAPACITY & CONSTRAINT REVEAL:
   - Expose utilization rates, expansion plans, or cash flow pressures

3. ONE COMPETITIVE PRESSURE QUESTION:
   - Create indirect competitive pressure through alternative supplier references

4. ONE CONTRACT LEVERAGE BUILDER:
   - Volume commitment reciprocity or payment term negotiation anchor

5. ONE VENDOR-SPECIFIC PRESSURE POINT:
   - Assess reliance on your business or identify switching costs

DESIGN PRINCIPLES:
- Open-ended questions that encourage detailed responses
- Psychologically comfortable but strategically revealing
- Include one follow-up probe for each question
- Prioritize questions that reveal maximum business intelligence

Provide exactly 5 strategically sequenced questions with tactical explanations and follow-up probes."""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content if hasattr(response, 'content') else str(response)
        print(f"✅ [QUESTION ARCHITECT] Question design complete")
        return {"strategic_questions": result}
    except Exception as e:
        print(f"❌ [QUESTION ARCHITECT] Error: {str(e)}")
        return {"strategic_questions": f"Error: {str(e)}", "error": str(e)}


def save_negotiation_logs_to_db(material_id: str, vendor_name: str, date: str, final_state: Dict[str, Any]):
    """Save negotiation LLM logs to database"""
    try:
        # Convert final_state to JSON, handling non-serializable objects
        logs_data = {
            "price_analysis": final_state.get("price_analysis", ""),  # Truncate for readability
            "procurement_strategy": final_state.get("procurement_strategy", ""),
            "negotiation_intelligence": final_state.get("negotiation_intelligence", ""),
            "strategic_questions": final_state.get("strategic_questions", ""),
            "error": final_state.get("error", "")
        }
        
        query = """
            INSERT INTO negotiation_llm_logs 
              (material_id, vendor_name, date, logs)
            VALUES 
              (%s, %s, %s, %s::jsonb)
            ON CONFLICT (material_id, vendor_name, date)
            DO UPDATE SET 
              logs = EXCLUDED.logs,
              created_at = CURRENT_TIMESTAMP
            RETURNING id, created_at;
        """
        
        result = database_query(query, [material_id, vendor_name, date, json.dumps(logs_data)])
        
        # Check for errors
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"❌ [LOGS SAVE ERROR] {result.get('error')}")
            return {"success": False, "error": result.get('error')}
        
        print(f"✅ [LOGS SAVED] Negotiation logs saved successfully")
        return {"success": True, "log_id": "N/A", "saved_at": datetime.utcnow().isoformat()}
    
    except Exception as e:
        print(f"❌ [LOGS SAVE ERROR] {str(e)}")
        return {"success": False, "error": str(e)}

# ======================
# 🚀 LangGraph Workflow
# ======================
def create_procurement_workflow():
    """Build LangGraph workflow"""
    workflow = StateGraph(ProcurementState)
    
    workflow.add_node("price_prediction", price_prediction_node)
    workflow.add_node("procurement_strategy", procurement_strategy_node)
    workflow.add_node("negotiation_intelligence", negotiation_intelligence_node)
    workflow.add_node("question_architecture", question_architecture_node)
    
    workflow.set_entry_point("price_prediction")
    workflow.add_edge("price_prediction", "procurement_strategy")
    workflow.add_edge("procurement_strategy", "negotiation_intelligence")
    workflow.add_edge("negotiation_intelligence", "question_architecture")
    workflow.add_edge("question_architecture", END)
    
    return workflow.compile()


# ======================
# 🧩 Lambda Handler
# ======================
def lambda_handler(event, context):
    """AWS Lambda handler with database integration"""
    start_time = time.perf_counter()
    
    try:
        # Parse event
        if isinstance(event, str):
            body = json.loads(event)
        else:
            body = event.get("body", event)
            if isinstance(body, str):
                body = json.loads(body)
        
        material_id = body.get("material_id")
        vendor_name = body.get("vendor_name")
        location_id = body.get("location_id")
        date = body.get("date")
        force_refresh = body.get("force_refresh", False)
        action = body.get("action", "negotiation_avoids")
        
        print(f"\n🚀 [WORKFLOW START] Action: {action}, Material: {material_id}, Vendor: {vendor_name}, Location: {location_id}, Date: {date}")
        
        # Check if recommendations already exist (skip if force_refresh)
        if not force_refresh:
            existing = check_existing_recommendations(vendor_name, date, material_id)
            if existing.get("exists"):
                strategy = existing.get("strategy", {})
                market_update = existing.get("market_update", {})
                
                has_avoids = strategy.get("whatWeWantToAvoid") and strategy.get("whatTheyWantToAvoid")
                has_questions = market_update.get("questionsToAsk")
                
                if has_avoids and has_questions:
                    print(f"✅ [CACHE HIT] Complete recommendations already exist, skipping generation")
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "success": True,
                            "cached": True,
                            "message": "Recommendations already exist",
                            "updated_at": existing.get("updated_at")
                        })
                    }
        
        # Fetch analysis data
        report = get_material_analysis(material_id, vendor_name, location_id)
        print(f"📦 [DATA FETCH] Material analysis loaded")
        
        # Initialize workflow
        graph = create_procurement_workflow()
        print(f"🔗 [WORKFLOW INIT] LangGraph workflow initialized")
        
        # Initial state
        initial_state: ProcurementState = {
            "material_id": material_id,
            "vendor_name": vendor_name,
            "location_id": location_id,
            "date": date,
            "report": report,
            "price_analysis": "",
            "procurement_strategy": "",
            "negotiation_intelligence": "",
            "strategic_questions": "",
            "error": ""
        }
        
        # Execute workflow
        print(f"\n📊 [WORKFLOW EXECUTION] Running 4-node analysis pipeline...\n")
        final_state = graph.invoke(initial_state)
        
        execution_time = time.perf_counter() - start_time
        print(f"\n✅ [WORKFLOW COMPLETE] Total execution time: {execution_time:.2f}s\n")
        
        # Parse negotiation_intelligence JSON
        strategy_results = {}
        try:
            negotiation_text = final_state.get("negotiation_intelligence", "")
            
            if "```json" in negotiation_text:
                json_start = negotiation_text.find("```json") + 7
                json_end = negotiation_text.find("```", json_start)
                negotiation_text = negotiation_text[json_start:json_end].strip()
            elif "```" in negotiation_text:
                json_start = negotiation_text.find("```") + 3
                json_end = negotiation_text.find("```", json_start)
                negotiation_text = negotiation_text[json_start:json_end].strip()
            
            json_start_idx = negotiation_text.find("{")
            json_end_idx = negotiation_text.rfind("}") + 1
            if json_start_idx != -1 and json_end_idx > json_start_idx:
                negotiation_text = negotiation_text[json_start_idx:json_end_idx]
            
            strategy_results = json.loads(negotiation_text)
            print(f"✅ Parsed negotiation intelligence: {strategy_results}")
        except json.JSONDecodeError as e:
            print(f"⚠️ [JSON PARSE ERROR] Could not parse negotiation_intelligence: {e}")
            strategy_results = {
                "buyerAvoid": ["Unable to parse - see raw analysis"],
                "supplierAvoid": ["Unable to parse - see raw analysis"]
            }
        
        # Extract questions from strategic_questions text
        questions_list = []
        try:
            questions_text = final_state.get("strategic_questions", "")
            import re
            question_pattern = r'\d+\.\s+(.+?)(?=\d+\.|$)'
            matches = re.findall(question_pattern, questions_text, re.DOTALL)
            
            if matches:
                for match in matches:
                    lines = match.strip().split('\n')
                    main_question = lines[0].strip()
                    main_question = main_question.replace('**', '').strip()
                    if main_question:
                        questions_list.append(main_question)
            
            if not questions_list:
                paragraphs = [p.strip() for p in questions_text.split('\n\n') if p.strip()]
                questions_list = [p for p in paragraphs if '?' in p][:5]
            
            print(f"✅ Extracted {len(questions_list)} questions")
        except Exception as e:
            print(f"⚠️ [QUESTION PARSE ERROR] Could not parse strategic_questions: {e}")
            questions_list = ["Unable to parse - see raw analysis"]

        # Format for database storage
        def format_array(arr):
            return "\n".join([f"• {item}" for item in arr]) if arr else None
        
        strategy = {
            "whatWeWantToAvoid": format_array(strategy_results.get("buyerAvoid", [])),
            "whatTheyWantToAvoid": format_array(strategy_results.get("supplierAvoid", []))
        }
        
        market_update = {
            "questionsToAsk": format_array(questions_list)
        }
        
        # Save to database
        db_result = save_recommendations_to_db(vendor_name, date, material_id, strategy, market_update)
        logs_result = save_negotiation_logs_to_db(material_id, vendor_name, date, final_state)

        if db_result.get("success"):
            print(f"✅ [DB SAVE SUCCESS] Recommendations saved to database")
        else:
            print(f"⚠️ [DB SAVE WARNING] Failed to save: {db_result.get('error')}")

        if logs_result.get("success"):
            print(f"✅ [LOGS SAVE SUCCESS] LLM logs saved to database (ID: {logs_result.get('log_id')})")
        else:
            print(f"⚠️ [LOGS SAVE WARNING] Failed to save logs: {logs_result.get('error')}")

        # Get material name
        material_name = get_material_name(material_id) if material_id else "Unknown Material"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "material_id": material_id,
                "material_name": material_name,
                "vendor_name": vendor_name,
                "location_id": location_id,
                "date": date,
                "strategy": strategy,
                "market_update": market_update,
                "db_saved": db_result.get("success"),
                "logs_saved": logs_result.get("success"),
                "log_id": logs_result.get("log_id"),
                "analysis_date": datetime.utcnow().isoformat(),
                "execution_time": f"{execution_time:.2f}s"
            }, indent=4, default=str)
        }
    
    except Exception as e:
        print(f"❌ [ERROR] {str(e)}")
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "trace": traceback.format_exc()
            })
        }

if __name__ == "__main__":
    test_event = {'material_id': '102089-000000', 'vendor_name': 'VADILAL CHEMICALS LIMITED', 'location_id': '212', 'date': '2025-10-15', 'action': 'negotiation_avoids', 'force_refresh': False}
    lambda_handler(test_event, None)