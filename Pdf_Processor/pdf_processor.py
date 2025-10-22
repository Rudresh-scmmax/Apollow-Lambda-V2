import os
import tempfile
import uuid
import json
from datetime import datetime
import boto3
from db_query import database_query
from extract_market_intelligence import capture_market_intelligence, DatabaseManager
from llm_module import generate_takeaways, query_bedrock_with_image, news_agent, classify_news_tags

from PIL import Image
import fitz  # PyMuPDF

S3_BUCKET = "private-bucket-fastapi"
s3 = boto3.client("s3")

def download_pdf_from_s3(key):
    tmp_path = os.path.join(tempfile.gettempdir(), os.path.basename(key))
    s3.download_file(S3_BUCKET, key, tmp_path)
    return tmp_path

def convert_pdf_to_images(pdf_path, max_dimension=1120):
    """
    Convert PDF pages to images compatible with Llama 3.2 Vision (max 1120x1120).
    Strictly cap both dimensions, split if necessary.
    """
    doc = fitz.open(pdf_path)
    images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        w, h = img.size

        # Step 1: Scale down if EITHER width OR height exceeds max_dimension
        if w > max_dimension or h > max_dimension:
            scale = max_dimension / max(w, h) * 0.95
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            w, h = img.size

        # Step 2: Split vertically if height still exceeds max_dimension
        if h > max_dimension:
            splits = (h // max_dimension) + 1
        else:
            splits = 1

        split_height = h // splits

        for s in range(splits):
            top = s * split_height
            bottom = h if s == splits - 1 else (s + 1) * split_height
            chunk = img.crop((0, top, w, bottom))

            # Step 3: Final check for BOTH dimensions
            cw, ch = chunk.size
            if cw > max_dimension or ch > max_dimension:
                safety_scale = max_dimension / max(cw, ch) * 0.95
                final_w = int(cw * safety_scale)
                final_h = int(ch * safety_scale)
                chunk = chunk.resize((final_w, final_h), Image.LANCZOS)

            chunk_path = os.path.join(tempfile.gettempdir(), f"page_{i}_part{s}.png")
            chunk.save(chunk_path, format='PNG', optimize=True)
            images.append(chunk_path)
    return images

def upload_images_to_s3(images, folder_prefix):
    s3_keys = []
    for img_path in images:
        filename = os.path.basename(img_path)
        s3_key = f"pdf-images/{folder_prefix}/{filename}"
        s3.upload_file(img_path, S3_BUCKET, s3_key)
        s3_keys.append(s3_key)
    return s3_keys

def cleanup_local_files(files):
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Failed to delete {f}: {e}")

def extract_text_from_pdf(s3_key):
    print("Processing PDF from S3 key:", s3_key)
    tmp_files = []
    try:
        pdf_path = download_pdf_from_s3(s3_key)
        tmp_files.append(pdf_path)

        images = convert_pdf_to_images(pdf_path, max_dimension=1120)
        tmp_files.extend(images)

        print(f"Converted {len(images)} pages to images.")

        all_text = []
        for i, img in enumerate(images):
            print(f"Processing page {i+1}/{len(images)}...")
            text = query_bedrock_with_image(img)
            all_text.append(text)
            print(f"Extracted {len(text)} characters from page {i+1}")

        folder_uuid = str(uuid.uuid4())
        upload_images_to_s3(images, folder_uuid)
        print(f"Uploaded images to S3 under folder: pdf-images/{folder_uuid}/")

        combined_text = "\n\n".join(all_text)
        print("Final extracted text length:", len(combined_text))

        return {
            "extracted_text": combined_text,
            "images_uploaded_to": f"pdf-images/{folder_uuid}/"
        }

    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

    finally:
        cleanup_local_files(tmp_files)


def lambda_handler(event, context):
    row_id = None
    tmp_dir = tempfile.mkdtemp()

    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        report_link = key

        head = s3.head_object(Bucket=bucket, Key=key)
        metadata = head.get('Metadata', {})
        row_id = int(metadata.get('rowid', '0'))
        print("row_id:", row_id)
        print("Processing S3 key:", key)

        # Check if this is a news file
        is_news_file = key.startswith('news/')

        # 1. Find material_id from market_research_status by row_id
        query = f"SELECT material_id FROM market_research_status WHERE id = {row_id}"
        result = database_query(query)
        body = json.loads(result["body"])
        material_id = body[0].get("material_id") if body else None
        if not material_id:
            print(f"No material_id found for row_id {row_id}")
            return {"statusCode": 400, "body": json.dumps({"message": "No material_id found for row_id"})}
        print(f"material_id: {material_id}")
        
        # 2. Get material_description from material_master
        query = f"SELECT material_description FROM material_master WHERE material_id = '{material_id}'"
        result = database_query(query)
        body = json.loads(result["body"])
        print(f"body: {body}")
        material_description = body[0].get("material_description") if body else None
        if not material_description:
            print(f"No material_description found for material_id {material_id}")
            return {"statusCode": 400, "body": json.dumps({"message": "No material_description found for id"})}

        # Get user_id
        query = f"SELECT user_id FROM market_research_status WHERE id = {row_id}"
        result = database_query(query)
        body = json.loads(result["body"])
        user_id = body[0].get("user_id") if body else ""
        print("user_id:", user_id)

        # 3. Extract text from file (PDF or news file)
        all_extracted_text = extract_text_from_pdf(key)["extracted_text"]

        # Check for text extraction
        if not all_extracted_text or len(all_extracted_text.strip()) < 50:
            print("WARNING: Very little or no text extracted from file")
            completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
            database_query(completed_query, ["failed - no text extracted", row_id])
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Failed to extract text from file"})
            }

        # Handle news files
        if is_news_file:
            print("Processing as news file...")
            
            # Extract news using news_agent
            news_items = news_agent(all_extracted_text, material_description, report_link)
            print(f"Extracted {len(news_items)} news items")
            
            # Insert news items into database
            db = DatabaseManager()
            inserted_count = 0
            for news_item in news_items:
                # Classify the news item to get the tag
                news_tag = classify_news_tags(news_item)
                print(f"[INFO] Classified news tag: {news_tag} for item: {news_item.get('title', 'Unknown')}")
                
                if db.insert_news_item(news_item, material_id, user_id, news_tag):
                    inserted_count += 1
                    print(f"[SUCCESS] Inserted news item: {news_item.get('title')}")
                else:
                    print(f"[WARNING] Failed to insert news item: {news_item.get('title')}")
            
            print(f"Successfully inserted {inserted_count} news items out of {len(news_items)}")
            
            # Update status
            completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
            database_query(completed_query, ["completed", row_id])
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "News processing complete",
                    "news_items_extracted": len(news_items),
                    "news_items_inserted": inserted_count
                })
            }

        # Handle PDF files (existing logic)
        print("Processing as PDF file...")
        
        # 4. Generate takeaways using the DB material
        takeaways = generate_takeaways(all_extracted_text, material_description)
        print("Takeaways JSON:", takeaways)

        try:
            parsed_takeaways = json.loads(takeaways)
            # Check for errors
            if "error" in parsed_takeaways:
                print("Error in takeaways generation:", parsed_takeaways["error"])
                completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
                database_query(completed_query, ["failed - takeaway generation error", row_id])
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "Failed to generate takeaways"})
                }

            published_date = parsed_takeaways.get("published_date")
            publication = parsed_takeaways.get("publication")
            takeaway_list = parsed_takeaways.get("takeaway_list", [])
            formatted_takeaways = "\n".join(takeaway_list)

            print("formatted_takeaways:", formatted_takeaways)

            # Insert report
            now = datetime.now().isoformat()
            insert_query = """
                INSERT INTO material_research_reports
                (date, publication, report_link, published_date, material_id, takeaway, upload_user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = [now, publication, report_link, published_date, material_id, formatted_takeaways, user_id]
            insert_result = database_query(insert_query, params)
            print("insert_result", insert_result)

            # Update status
            completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
            database_query(completed_query, ["completed", row_id])

            # Capture market intelligence (best effort)
            try:
                print(f"all_extracted_text: {all_extracted_text}")
                capture_market_intelligence(all_extracted_text, report_link, user_id, material_description, material_id)
            except Exception as mi_error:
                print(f"Error capturing market intelligence: {mi_error}")

        except Exception as error:
            print("Error processing JSON:", error)
            import traceback
            traceback.print_exc()
            completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
            database_query(completed_query, ["failed", row_id])
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Invalid JSON returned from generateTakeaways",
                    "error": str(error),
                }),
            }

        return {"statusCode": 200, "body": json.dumps({"message": "Takeaways processed"})}

    except Exception as error:
        print("Error in lambda_handler:", error)
        import traceback
        traceback.print_exc()
        if row_id:
            completed_query = "UPDATE market_research_status SET status = %s WHERE id = %s"
            database_query(completed_query, ["failed", row_id])
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal error", "error": str(error)})
        }

# For local testing
if __name__ == "__main__":
    lambda_handler({
        "Records": [{
            "s3": {
                "bucket": {"name": "private-bucket-fastapi"},
                "object": {"key": "pdfs/d1ccc743-29bb-40d6-b937-060a2962db17.pdf"}
            }
        }]
    }, None)
