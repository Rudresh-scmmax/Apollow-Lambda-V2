from datetime import datetime, date, timezone
import json
from db_query import database_query
# Assuming the updated extract_demand_supply_outlook_agent is now in llm_module
from llm_module import extract_demand_supply_outlook_agent, news_agent, classify_news_tags, summarize_demand_supply_with_bedrock 

class DatabaseManager:
    def get_material_id(self, material):
        """Fetches material_id from material_master table."""
        try:
            query = f"SELECT material_id FROM material_master WHERE material_description = '{material}'"
            result = database_query(query)

            body = json.loads(result["body"])
            material_id = body[0].get("material_id") if body else None
            return material_id
        except Exception as e:
            print(f"[ERROR] Failed to get material_id for '{material}': {e}")
            return None

    def get_location_id(self, region):
        """Fetches location_id from location_master table."""
        try:
            result = database_query(
                "SELECT location_id FROM location_master WHERE location_name = %s",
                [region]
            )
            body = json.loads(result["body"])
            location_id = body[0].get("location_id") if body else None
            return location_id
        
        except Exception as e:
            print(f"[ERROR] Failed to get location_id for '{region}': {e}")
            return None

    
    def insert_supply_trend(self, outlook_item, material_id, report_url, user_id):
        """Inserts a single supply outlook item into demand_supply_trends."""
        try:
            location_id = self.get_location_id(outlook_item["region"])
            published_date = outlook_item.get("published_date")
            if published_date and isinstance(published_date, str):
                try:
                    published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
                except ValueError:
                    print(f"[WARNING] Invalid published_date format: {published_date}")
                    published_date = None

            # Convert date to string for JSON serialization
            if published_date and isinstance(published_date, date):
                published_date = published_date.isoformat()

            source_link = outlook_item.get("source_link")
            if source_link and not isinstance(source_link, str):
                source_link = None

            database_query(
                """
                INSERT INTO demand_supply_trends (
                    upload_date, source, source_link, source_published_date,
                    material_id, upload_user_id,
                    supply_impact, location_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    datetime.now(timezone.utc).date().isoformat(),
                    'Report',
                    report_url,
                    published_date,
                    material_id,
                    user_id,
                    outlook_item["impact_text"],
                    location_id
                ]
            )
            print(f"[SUCCESS] Inserted supply outlook for material_id={material_id}, location_id={location_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Supply insert failed for {outlook_item}: {e}")
            return False


    def insert_demand_trend(self, outlook_item, material_id, report_url, user_id):
        """Inserts a single demand outlook item into demand_supply_trends."""
        try:
            location_id = self.get_location_id(outlook_item["region"])
            published_date = outlook_item.get("published_date")
            if published_date and isinstance(published_date, str):
                try:
                    published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
                except ValueError:
                    print(f"[WARNING] Invalid published_date format: {published_date}")
                    published_date = None

            # Convert date to string for JSON serialization
            if published_date and isinstance(published_date, date):
                published_date = published_date.isoformat()
            

            # Ensure source_link is handled correctly
            source_link = outlook_item.get("source_link")
            if source_link and not isinstance(source_link, str):
                source_link = None # Ensure it's a string or None


            database_query(
                """
                INSERT INTO demand_supply_trends (
                    upload_date, source, source_link, source_published_date,
                    material_id, upload_user_id,
                    demand_impact, location_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    datetime.now(timezone.utc).date().isoformat(),
                    'Report',
                    report_url,
                    published_date,
                    material_id,
                    user_id,
                    outlook_item["impact_text"],
                    location_id
                ]
            )
            print(f"[SUCCESS] Inserted demand outlook for material_id={material_id}, location_id={location_id}")
            return True
        except Exception as e:
            print(f"[ERROR] Demand insert failed for {outlook_item}: {e}")
            return False
        
    
    def insert_news_item(self, news_item, material_id, user_id, news_tag=""):
        """Inserts a single news item into the news_insights table."""
        try:
            location_id = self.get_location_id(news_item["region"])
            published_date = news_item.get("published_date")
            if published_date and isinstance(published_date, str):
                try:
                    published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
                except ValueError:
                    print(f"[WARNING] Invalid published_date format: {published_date}")
                    published_date = None

            # Convert date to string for JSON serialization
            if published_date and isinstance(published_date, date):
                published_date = published_date.isoformat()

            # Source link fallback
            source_link = news_item.get("news_url")
            if source_link and not isinstance(source_link, str):
                source_link = None

            # Perform DB insert
            database_query(
                """
                INSERT INTO news_insights (
                    published_date, source, source_link, title,
                    material_id, location_id, upload_user_id, news_tag
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    published_date,
                    "Report",
                    source_link,
                    news_item["title"],
                    material_id,
                    location_id,
                    user_id,
                    news_tag
                ]
            )

            print(f"[SUCCESS] Inserted news item for material_id={material_id}, location_id={location_id}, tag={news_tag}")
            return True

        except Exception as e:
            print(f"[ERROR] News insert failed for {news_item}: {e}")
            return False

    def get_demand_supply_data(self, material_id, location_id, summary_date):
        """
        Retrieves all demand and supply impact data for a specific material, location, and date.
        
        Args:
            material_id (str): Material ID
            location_id (int): Location ID  
            summary_date (str): Date in YYYY-MM-DD format
            
        Returns:
            dict: Contains 'demand_data' and 'supply_data' lists
        """
        try:
            # Get demand impact data
            demand_query = """
            SELECT demand_impact, source_published_date, source, source_link
            FROM demand_supply_trends 
            WHERE material_id = %s AND location_id = %s 
            AND DATE(source_published_date) = %s 
            AND demand_impact IS NOT NULL
            ORDER BY source_published_date DESC
            """
            
            demand_result = database_query(demand_query, [material_id, location_id, summary_date])
            demand_data = json.loads(demand_result["body"]) if demand_result.get("body") else []
            
            # Get supply impact data
            supply_query = """
            SELECT supply_impact, source_published_date, source, source_link
            FROM demand_supply_trends 
            WHERE material_id = %s AND location_id = %s 
            AND DATE(source_published_date) = %s 
            AND supply_impact IS NOT NULL
            ORDER BY source_published_date DESC
            """
            
            supply_result = database_query(supply_query, [material_id, location_id, summary_date])
            supply_data = json.loads(supply_result["body"]) if supply_result.get("body") else []
            
            return {
                'demand_data': demand_data,
                'supply_data': supply_data
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to retrieve demand/supply data: {e}")
            return {'demand_data': [], 'supply_data': []}

    def upsert_demand_supply_summary(self, material_id, location_id, summary_date, demand_summary, supply_summary, combined_summary, demand_count, supply_count):
        """
        Inserts or updates a summary record in demand_supply_summary table.
        Uses PostgreSQL UPSERT (ON CONFLICT) for upsert functionality.
        
        Args:
            material_id (str): Material ID
            location_id (int): Location ID
            summary_date (str): Date in YYYY-MM-DD format
            demand_summary (str): Demand summary text
            supply_summary (str): Supply summary text
            combined_summary (str): Combined summary text
            demand_count (int): Number of demand records
            supply_count (int): Number of supply records
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # PostgreSQL UPSERT syntax
            upsert_query = """
            INSERT INTO demand_supply_summary (
                material_id, location_id, summary_date, 
                demand_summary, supply_summary, combined_summary,
                demand_count, supply_count, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (material_id, location_id, summary_date) 
            DO UPDATE SET
                demand_summary = EXCLUDED.demand_summary,
                supply_summary = EXCLUDED.supply_summary,
                combined_summary = EXCLUDED.combined_summary,
                demand_count = EXCLUDED.demand_count,
                supply_count = EXCLUDED.supply_count,
                updated_at = EXCLUDED.updated_at
            """
            
            # Convert datetime to string for JSON serialization
            current_time = datetime.now(timezone.utc).isoformat()
            
            database_query(upsert_query, [
                material_id, location_id, summary_date,
                demand_summary, supply_summary, combined_summary,
                demand_count, supply_count, current_time, current_time
            ])
            
            print(f"[SUCCESS] Upserted summary for material_id={material_id}, location_id={location_id}, date={summary_date}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to upsert summary: {e}")
            return False

    def process_demand_supply_summary(self, material_id, location_id, summary_date):
        """
        Processes demand and supply data to create/update summary in demand_supply_summary table.
        
        Args:
            material_id (str): Material ID
            location_id (int): Location ID
            summary_date (str): Date in YYYY-MM-DD format
            
        Returns:
            dict: Result with success status and summary data
        """
        try:
            # Step 1: Get demand and supply data
            data = self.get_demand_supply_data(material_id, location_id, summary_date)
            demand_data = data['demand_data']
            supply_data = data['supply_data']
            
            # Step 2: Summarize with Bedrock
            summaries = summarize_demand_supply_with_bedrock(
                demand_data, supply_data, material_id, location_id, summary_date
            )
            
            # Step 3: Upsert the summary
            success = self.upsert_demand_supply_summary(
                material_id=material_id,
                location_id=location_id,
                summary_date=summary_date,
                demand_summary=summaries['demand_summary'],
                supply_summary=summaries['supply_summary'],
                combined_summary=summaries['combined_summary'],
                demand_count=len(demand_data),
                supply_count=len(supply_data)
            )
            
            if success:
                return {
                    'success': True,
                    'message': f'Summary processed successfully for material_id={material_id}, location_id={location_id}, date={summary_date}',
                    'data': {
                        'material_id': material_id,
                        'location_id': location_id,
                        'summary_date': summary_date,
                        'demand_count': len(demand_data),
                        'supply_count': len(supply_data),
                        'summaries': summaries
                    }
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to process summary for material_id={material_id}, location_id={location_id}, date={summary_date}',
                    'data': None
                }
                
        except Exception as e:
            print(f"[ERROR] Failed to process summary: {e}")
            return {
                'success': False,
                'message': f'Error processing summary: {str(e)}',
                'data': None
            }


def capture_market_intelligence(plain_text, report_url, user_id, material, material_id):
    """
    AWS Lambda handler to process extracted text for supply/demand outlook.
    It extracts material and region, queries database for IDs,
    then uses LLM to get supply/demand outlooks, and finally inserts them into DB.
    """

    db = DatabaseManager()


    if not material_id:
        print(f"[ERROR] Material '{material}' (ID: {material_id}) not found in master table.")
        return {'statusCode': 400, 'body': "Material not found in master table. Please ensure master data is populated."}

    try:
        # Step 3: Use the combined agent to get both demand and supply outlooks
        # The new agent returns {"demand": [...], "supply": [...]}
        combined_outlook = extract_demand_supply_outlook_agent(plain_text, material)
        
        supply_outlook_items = combined_outlook.get("supply", [])
        demand_outlook_items = combined_outlook.get("demand", [])

        print(f"Extracted Supply Outlook Items: {supply_outlook_items}")
        print(f"Extracted Demand Outlook Items: {demand_outlook_items}")

        inserted_supply_count = 0
        for outlook_item in supply_outlook_items:
            if db.insert_supply_trend(outlook_item, material_id, report_url, user_id):
                inserted_supply_count += 1
            else:
                print(f"[WARNING] Skipping problematic supply outlook item: {outlook_item}")

        inserted_demand_count = 0
        for outlook_item in demand_outlook_items:
            # The 'outlook_item' itself contains 'impact_text', 'published_date', 'report_url', 'material'
            if db.insert_demand_trend(outlook_item, material_id, report_url, user_id):
                inserted_demand_count += 1
            else:
                print(f"[WARNING] Skipping problematic demand outlook item: {outlook_item}")

        print(f"Summary: Successfully inserted {inserted_supply_count} supply and {inserted_demand_count} demand outlooks.")

        # Process demand/supply summary after inserting data
        summary_results = []
        if inserted_supply_count > 0 or inserted_demand_count > 0:
            # Get unique location_ids and dates from the inserted data
            processed_combinations = set()
            
            for outlook_item in supply_outlook_items + demand_outlook_items:
                location_id = db.get_location_id(outlook_item["region"])
                published_date = outlook_item.get("published_date")
                
                if location_id and published_date:
                    combination_key = f"{material_id}_{location_id}_{published_date}"
                    if combination_key not in processed_combinations:
                        processed_combinations.add(combination_key)
                        
                        # Process summary for this combination
                        summary_result = db.process_demand_supply_summary(
                            material_id, location_id, published_date
                        )
                        summary_results.append(summary_result)
                        
                        if summary_result['success']:
                            print(f"[SUCCESS] Created/updated summary for material_id={material_id}, location_id={location_id}, date={published_date}")
                        else:
                            print(f"[WARNING] Failed to create summary: {summary_result['message']}")

        news_insights = news_agent(plain_text, material, report_url)
        print(f"Extracted News Insights: {news_insights}")
        for news_item in news_insights:
            # Classify the news item to get the tag
            news_tag = classify_news_tags(news_item)
            print(f"[INFO] Classified news tag: {news_tag} for item: {news_item.get('title', 'Unknown')}")
            
            if db.insert_news_item(news_item, material_id, user_id, news_tag):
                print(f"[SUCCESS] Inserted news item: {news_item}")
            else:
                print(f"[WARNING] Failed to insert news item: {news_item}")

        return {
            'statusCode': 200,
            'body': json.dumps({ # Return a JSON string as the body
                'message': 'Outlook extraction and insertion complete.',
                'material': material,
                'material_id': material_id,
                'extracted_supply_outlooks': supply_outlook_items,
                'extracted_demand_outlooks': demand_outlook_items,
                'summary_results': summary_results
            })
        }

    except Exception as e:
        print(f"[CRITICAL ERROR] Lambda handler failed: {str(e)}")
        return {'statusCode': 500, 'body': f"An unexpected error occurred: {str(e)}"}



# db = DatabaseManager()
# data = [{'title': 'Glycerine prices surge in Asia-Pacific due to supply constraints in Malaysia and Indonesia', 'published_date': '2024-06-30', 'material': 'Glycerine', 'region': 'Asia-Pacific', 'news_url': 'https://subscriber.icis.com/report/sample-glycerine-report-2025'}, {'title': 'Strong demand from pharmaceutical and personal care sectors in India and Southeast Asia boosts Glycerine prices', 'published_date': '2024-06-30', 'material': 'Glycerine', 'region': 'Asia-Pacific', 'news_url': 'https://subscriber.icis.com/report/sample-glycerine-report-2025'}, {'title': 'Chinese glycerine exports decline by 12% due to stricter port inspections and increased domestic consumption', 'published_date': '2024-06-30', 'material': 'Glycerine', 'region': 'Asia-Pacific', 'news_url': 'https://subscriber.icis.com/report/sample-glycerine-report-2025'}, {'title': 'Indonesia considers policy prioritizing domestic glycerine use, potentially restricting regional supply', 'published_date': '2024-06-30', 'material': 'Glycerine', 'region': 'Asia-Pacific', 'news_url': 'https://subscriber.icis.com/report/sample-glycerine-report-2025'}, {'title': 'Logistical delays in Glycerine transport monitored due to increased monsoon activity in India', 'published_date': '2024-06-30', 'material': 'Glycerine', 'region': 'Asia-Pacific', 'news_url': 'https://subscriber.icis.com/report/sample-glycerine-report-2025'}]
# for item in data:
#     material_id = db.get_material_id(item['material'])
#     location_id = db.get_location_id(item['region'])
#     if material_id and location_id:
#         db.insert_news_item(item, material_id, location_id, 1)  # Assuming user_id is 1 for testing
#     else:
#         print(f"Material or location not found for item: {item}")



[{'published_date': '2025-09-18', 'source_link': 'https://subscriber.icis.com/commodity/issue/view/petchem%2Fpublication-262/petchem%2Fissue-f-glycerine-20250918', 'impact_text': 'Demand for refined glycerine in drums saw higher offers due to restocking activities for customers in the Middle East and the US.', 'material': 'Glycerine', 'region': 'Middle East, US'}, {'published_date': '2025-09-18', 'source_link': 'https://subscriber.icis.com/commodity/issue/view/petchem%2Fpublication-262/petchem%2Fissue-f-glycerine-20250918', 'impact_text': 'Buyers in China and India have largely covered their October and some November requirements, regional producers have been focusing on other markets outside of China and India.', 'material': 'Glycerine', 'region': 'China, India, Asia-Pacific'}]