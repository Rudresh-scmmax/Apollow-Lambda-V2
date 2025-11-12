import json
import os
import base64
import boto3
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
import hashlib
from rapidfuzz import process, fuzz
from typing import Optional
from db_query import database_query

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

# === AWS Bedrock Setup ===
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ARNs
TEXT_MODEL_ARN = "arn:aws:bedrock:us-east-1:127214171089:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0"


def invoke_bedrock_text(system_msg, user_content, temperature=0.1, max_tokens=4096):
    """
    Invoke Bedrock's Llama 4 Scout text model using Converse API.
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {"text": user_content.strip()}
                ]
            }
        ]
        
        response = bedrock.converse(
            modelId=TEXT_MODEL_ARN,
            messages=messages,
            system=[{"text": system_msg.strip()}],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9
            }
        )
        
        # Extract text from response
        text = ""
        if response.get('output') and response['output'].get('message'):
            content = response['output']['message'].get('content', [])
            if content and len(content) > 0:
                text = content[0].get('text', '')
        
        return text
        
    except Exception as e:
        print(f"Bedrock invocation failed: {e}")
        return None


class DatabaseManager:
    def __init__(self):
        pass

    def _parse_db_result(self, result):
        """Helper to parse database_query results"""
        # Check for errors first
        if isinstance(result, dict) and result.get('statusCode') == 500:
            print(f"Database query error: {result.get('error')}")
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

    def _get_material_id(self, material: Optional[str],
                       score_cutoff: int = 80) -> Optional[str]:
        """
        Return the best-matching material_id using RapidFuzz.
        If nothing meets score_cutoff or material is None/blank, return None.
        """
        if not material:
            return None

        query = "SELECT material_id, material_description FROM material_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        choices = {r["material_description"]: r["material_id"] for r in rows}

        best = process.extractOne(
            material,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None
    
    def _get_supplier_id(self, supplier: Optional[str],
                       score_cutoff: int = 80) -> Optional[int]:
        """
        Return the best-matching supplier_id using RapidFuzz.
        If nothing meets score_cutoff or supplier is None/blank, return None.
        """
        if not supplier:
            return None

        query = "SELECT supplier_id, supplier_name, supplier_plant_name FROM supplier_master"
        result = database_query(query)
        rows = self._parse_db_result(result)
        
        if not rows:
            return None

        # Create choices from both supplier_name and supplier_plant_name
        choices = {}
        for r in rows:
            if r["supplier_name"]:
                choices[r["supplier_name"]] = r["supplier_id"]
            if r["supplier_plant_name"]:
                choices[r["supplier_plant_name"]] = r["supplier_id"]

        best = process.extractOne(
            supplier,
            choices.keys(),
            scorer=fuzz.WRatio,
            processor=str.lower,
            score_cutoff=score_cutoff,
        )
        return choices[best[0]] if best else None
    
    def insert_email(self, gmail_id, sender, subject, body, received_at):
        try:
            # Convert datetime to ISO format string for JSON serialization
            if isinstance(received_at, datetime):
                received_at_str = received_at.isoformat()
            else:
                received_at_str = received_at
            
            query = """
                INSERT INTO emails (gmail_id, sender, subject, body, received_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO NOTHING
            """
            print(f"[LOG] Attempting to insert email: gmail_id={gmail_id}, subject={subject[:50]}...")
            result = database_query(query, [gmail_id, sender, subject, body, received_at_str])
            
            # Check for errors - Lambda might return different formats
            if isinstance(result, dict):
                # Check for error status codes
                if result.get('statusCode') == 500 or result.get('statusCode') == 400:
                    error_msg = result.get('error', result.get('body', 'Unknown error'))
                    print(f"[ERROR] Failed to insert email: {error_msg}")
                    print(f"[DEBUG] Full result: {result}")
                # Check if it's a successful response with body
                elif 'body' in result:
                    try:
                        body_data = json.loads(result['body']) if isinstance(result['body'], str) else result['body']
                        print(f"[LOG] Email inserted successfully: gmail_id={gmail_id}")
                    except:
                        print(f"[LOG] Email inserted successfully: gmail_id={gmail_id}")
                elif result.get('statusCode') == 200:
                    print(f"[LOG] Email inserted successfully: gmail_id={gmail_id}")
                else:
                    # Assume success if no error status code
                    print(f"[LOG] Email inserted successfully: gmail_id={gmail_id}")
            else:
                # Non-dict result might be a success indicator
                print(f"[LOG] Email inserted successfully: gmail_id={gmail_id}")
        except Exception as e:
            print(f"[ERROR] Failed to insert email: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        
    def insert_mom(self, gmail_id, date, supplier, link_to_mom, key_takeaway, region, material):
        try:
            material_id = self._get_material_id(material)
            supplier_id = self._get_supplier_id(supplier)

            print(f"[LOG] Attempting to insert MoM: gmail_id={gmail_id}, date={date}, supplier={supplier}, link_to_mom={link_to_mom}, key_takeaway={key_takeaway}, region={region}, material_id={material_id}, supplier_id={supplier_id}")

            query = """
                INSERT INTO meeting_minutes (gmail_id, date, supplier, supplier_id, link_to_mom, key_takeaway, region, material_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO NOTHING
            """
            result = database_query(query, [gmail_id, date, supplier, supplier_id, link_to_mom, key_takeaway, region, material_id])
            if isinstance(result, dict) and result.get('statusCode') == 500:
                error_msg = result.get('error', 'Unknown error')
                print(f"[ERROR] Failed to insert MoM: {error_msg}")
            else:
                print("[LOG] Insert committed.")
        except Exception as e:
            print(f"[ERROR] Failed to insert MoM: {str(e)}")

    def insert_jdp(self, gmail_id, supplier, project, mom_link, key_takeaway, next_action_point, responsibility, region, material):
        try:
            material_id = self._get_material_id(material)
            supplier_id = self._get_supplier_id(supplier)

            # Convert responsibility to JSON string if it's a dict or list
            if isinstance(responsibility, (dict, list)):
                responsibility_str = json.dumps(responsibility)
            else:
                responsibility_str = responsibility

            # Convert next_action_point to JSON string if it's a list
            if isinstance(next_action_point, list):
                next_action_point_str = json.dumps(next_action_point)
            else:
                next_action_point_str = next_action_point

            query = """
                INSERT INTO joint_development_projects
                (gmail_id, supplier, supplier_id, project, mom_link, key_takeaway, next_action_point, responsibility, region, material_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO NOTHING
            """
            result = database_query(query, [gmail_id, supplier, supplier_id, project, mom_link, key_takeaway, next_action_point_str, responsibility_str, region, material_id])
            if isinstance(result, dict) and result.get('statusCode') == 500:
                error_msg = result.get('error', 'Unknown error')
                print(f"[ERROR] Failed to insert JDP: {error_msg}")
            else:
                print("[LOG] JDP Insert committed.")
        except Exception as e:
            print(f"[ERROR] Failed to insert JDP: {str(e)}")
    
    def insert_mpe(self, gmail_id, date, supplier, event, mom_link, key_takeaway, photos_link, region, material):
        try:
            material_id = self._get_material_id(material)
            supplier_id = self._get_supplier_id(supplier)

            query = """
                INSERT INTO multiple_point_engagements
                (gmail_id, date, supplier, supplier_id, event, mom_link, key_takeaway, photos_link, region, material_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO NOTHING
            """
            result = database_query(query, [gmail_id, date, supplier, supplier_id, event, mom_link, key_takeaway, photos_link, region, material_id])
            if isinstance(result, dict) and result.get('statusCode') == 500:
                error_msg = result.get('error', 'Unknown error')
                print(f"[ERROR] Failed to insert MPE: {error_msg}")
            else:
                print("[LOG] MPE Insert committed.")
        except Exception as e:
            print(f"[ERROR] Failed to insert MPE: {str(e)}")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        raise Exception("token.json not found. Run OAuth flow locally and upload token.json with your deployment package.")
    return build('gmail', 'v1', credentials=creds)

def get_email_body(payload):
    def decode_base64(data):
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    if payload.get('mimeType') == 'text/plain' and 'data' in payload.get('body', {}):
        return decode_base64(payload['body']['data'])
    if payload.get('mimeType', '').startswith('multipart/'):
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                return decode_base64(part['body']['data'])
    return "(No plain text body found)"

def extract_json_from_response(response_text):
    """
    Extract JSON from Bedrock response, handling cases where there's extra text before/after JSON.
    Returns the parsed JSON object or None if extraction fails.
    """
    if not response_text or not response_text.strip():
        return None
    
    # Clean up markdown code blocks if present
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    # Try to find JSON by looking for balanced braces/brackets
    def find_balanced_json(text, start_char='{', end_char='}'):
        """Find the first complete JSON structure with balanced braces/brackets"""
        count = 0
        start_idx = -1
        in_string = False
        escape_next = False
        
        for i, char in enumerate(text):
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
            
            if in_string:
                continue
            
            if char == start_char:
                if count == 0:
                    start_idx = i
                count += 1
            elif char == end_char:
                count -= 1
                if count == 0 and start_idx != -1:
                    try:
                        json_str = text[start_idx:i+1]
                        parsed = json.loads(json_str)
                        return parsed
                    except json.JSONDecodeError:
                        start_idx = -1
                        continue
        return None
    
    # Try to find JSON object first
    result = find_balanced_json(response_text, '{', '}')
    if result is not None:
        return result
    
    # Try to find JSON array
    result = find_balanced_json(response_text, '[', ']')
    if result is not None:
        return result
    
    # Last resort: try parsing the entire response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return None

def extract_mom_structured(subject, body):
    """
    Use Bedrock to extract structured MoM data, including region and material, from the email.
    Returns a dict with keys: date, supplier, link_to_mom, key_takeaway, region, material.
    """
    system_msg = """You are an intelligent assistant extracting structured data from emails.

Extract ONLY if the email is a summary of a meeting, contains minutes of meeting (MoM), or explicitly documents a discussion with clear outcomes, action points, or responsibilities. Do NOT extract for general business correspondence, quotations, or informal discussions.

Return a valid JSON object with these fields: date, supplier, link_to_mom, key_takeaway, region, material.
- Only extract if the email is a formal meeting summary, MoM, or contains explicit meeting outcomes and action points.
- Do NOT extract for quotations, proposals, or general business emails.
- Do NOT guess or fabricate values — return null if a field is not explicitly found.
- If the email contains placeholder text like [Insert Date] or [Your Company Name], still extract it as a meeting email if it has the structure of meeting minutes.
- If it is not a meeting-related email, return null."""

    user_content = f"""
**Email Subject**: {subject}

**Email Body**:
{body}
"""
    try:
        print(f"[DEBUG] Invoking Bedrock for MoM extraction...")
        result = invoke_bedrock_text(system_msg, user_content, temperature=0.1, max_tokens=4096)
        
        if not result:
            print("[DEBUG] Bedrock returned empty result")
            return None
        
        # Check for explicit "not a meeting" response, but be more lenient
        if result and ("Not a meeting email" in result or ("null" in result.lower() and "not a meeting" in result.lower())):
            print(f"[DEBUG] Bedrock indicated this is not a meeting email")
            print(f"[DEBUG] Full Bedrock response: {result}")
            return None
        
        print(f"[DEBUG] Bedrock response length: {len(result)} characters")
        print(f"[DEBUG] Bedrock response preview: {result[:200]}...")
        
        mom_data = extract_json_from_response(result)
        
        # Check if mom_data is None or not a dict
        if not mom_data or not isinstance(mom_data, dict):
            print(f"[DEBUG] Failed to extract JSON from Bedrock response. mom_data type: {type(mom_data)}")
            return None
        
        # Check if all values are None/null
        if not any(mom_data.values()):
            print(f"[DEBUG] All MoM data values are None/null: {mom_data}")
            return None
        
        print(f"[DEBUG] Successfully extracted MoM data: {mom_data}")
        return mom_data
    except (json.JSONDecodeError, AttributeError, TypeError, Exception) as e:
        print(f"[ERROR] Bedrock MoM extraction failed: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return None


# Add below your extract_mom_structured function
def extract_jdp_structured(subject, body):
    """
    Use Bedrock to extract structured Joint Development Project (JDP) data from the email.
    Returns a dict with keys: supplier, project, key_takeaway, next_action_point, responsibility, region, material.
    """
    system_msg = """You are an intelligent assistant extracting structured data from emails.

Extract ONLY if the email is clearly about a Joint Development Project (JDP), such as project kickoff, progress updates, or meetings specifically mentioning a JDP. Ignore unrelated emails, general business discussions, or quotations.

Return a valid JSON object with these fields: supplier, project, key_takeaway, next_action_point, responsibility, region, material.
- Only extract if the email is specifically about a Joint Development Project (JDP).
- Do NOT extract for general meetings, quotations, or unrelated business emails.
- Do NOT guess or fabricate values — return null if a field is not explicitly found.
- If it is not a JDP-related email, return null."""

    user_content = f"""
**Email Subject**: {subject}

**Email Body**:
{body}
"""
    try:
        result = invoke_bedrock_text(system_msg, user_content, temperature=0.1, max_tokens=4096)
        if not result or "Not a JDP email" in result or "null" in result.lower():
            return None
        
        jdp_data = extract_json_from_response(result)
        
        # Check if jdp_data is None or not a dict
        if not jdp_data or not isinstance(jdp_data, dict):
            return None
        
        if not any(jdp_data.values()):
            return None
            
        return jdp_data
    except (json.JSONDecodeError, AttributeError, TypeError, Exception) as e:
        print(f"[ERROR] Bedrock JDP extraction failed: {e}")
        return None


def extract_mpe_structured(subject, body):
    """
    Use Bedrock to extract structured Multiple Point Engagement (MPE) data from the email.
    Returns a dict with keys: date, supplier, event, key_takeaway, photos_link, region, material.
    """
    system_msg = """You are an intelligent assistant extracting structured data from emails.

Extract ONLY if the email is about a Multiple Point Engagement (MPE) event, such as plant visits, technical workshops, supplier events, or multi-party technical engagements. Ignore general meetings, project updates, or quotations.

Return a valid JSON object with these fields: date, supplier, event, key_takeaway, photos_link, region, material.
- Only extract if the email is about a Multiple Point Engagement (MPE) event.
- Do NOT extract for general meetings, project updates, or quotations.
- Do NOT guess or fabricate values — return null if a field is not explicitly found.
- If it is not an MPE-related email, return null."""

    user_content = f"""
**Email Subject**: {subject}

**Email Body**:
{body}
"""
    try:
        result = invoke_bedrock_text(system_msg, user_content, temperature=0.1, max_tokens=4096)
        if not result or "Not an MPE email" in result or "null" in result.lower():
            return None
        
        mpe_data = extract_json_from_response(result)
        
        # Check if mpe_data is None or not a dict
        if not mpe_data or not isinstance(mpe_data, dict):
            return None
        
        if not any(mpe_data.values()):
            return None
            
        return mpe_data
    except (json.JSONDecodeError, AttributeError, TypeError, Exception) as e:
        print(f"[ERROR] Bedrock MPE extraction failed: {e}")
        return None
    

def auto_mail_process(limit=5):
    """
    Fetch and process emails from Gmail inbox.
    
    Args:
        limit: Maximum number of emails to fetch and process (default: 10)
    """
    db_manager = DatabaseManager()
    service = get_gmail_service()
    messages = []
    
    # Fetch messages with limit
    max_results = min(limit, 50)  # Gmail API max is 500 per request
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages.extend(results.get('messages', []))

    # Paginate only if we haven't reached the limit
    while 'nextPageToken' in results and len(messages) < limit:
        remaining = limit - len(messages)
        if remaining <= 0:
            break
        results = service.users().messages().list(
            userId='me',
            maxResults=min(remaining, 50),
            pageToken=results['nextPageToken']
        ).execute()
        messages.extend(results.get('messages', []))

    # Limit the messages to process
    messages = messages[:limit]
    
    print(f"[LOG] Processing {len(messages)} emails (limit: {limit})")
    
    inserted = 0
    for i, msg in enumerate(messages, 1):
        try:
            print(f"[LOG] Processing email {i}/{len(messages)}: gmail_id={msg['id']}")
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            internal_date = int(msg_data.get('internalDate', 0)) // 1000
            received_at = datetime.fromtimestamp(internal_date, tz=timezone.utc)

            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
            gmail_id = msg['id']
            body = get_email_body(msg_data['payload'])

            print(f"[LOG] Email details - Subject: {subject[:50]}..., Sender: {sender[:50]}...")
            db_manager.insert_email(gmail_id, sender, subject, body, received_at)
            inserted += 1
            
            # Extract and insert structured data
            try:
                mom_data = extract_mom_structured(subject, body)
                if mom_data:
                    link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
                    db_manager.insert_mom(
                        gmail_id=gmail_id,
                        date=mom_data.get("date"),
                        supplier=mom_data.get("supplier"),
                        link_to_mom=link_to_mom,
                        key_takeaway=mom_data.get("key_takeaway"),
                        region=mom_data.get("region"),
                        material=mom_data.get("material")
                    )
                    print(f"\n[STRUCTURED MOM DATA]\n{mom_data}\n")
            except Exception as e:
                print(f"[ERROR] Failed to extract/insert MoM: {e}")
            
            try:
                jdp_data = extract_jdp_structured(subject, body)
                if jdp_data:
                    link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
                    db_manager.insert_jdp(
                        gmail_id=gmail_id,
                        supplier=jdp_data.get("supplier"),
                        project=jdp_data.get("project"),
                        mom_link=link_to_mom,
                        key_takeaway=jdp_data.get("key_takeaway"),
                        next_action_point=jdp_data.get("next_action_point"),
                        responsibility=jdp_data.get("responsibility"),
                        region=jdp_data.get("region"),
                        material=jdp_data.get("material")
                    )
                    print(f"\n[STRUCTURED JDP DATA]\n{jdp_data}\n")
            except Exception as e:
                print(f"[ERROR] Failed to extract/insert JDP: {e}")
            
            try:
                mpe_data = extract_mpe_structured(subject, body)
                if mpe_data:
                    link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
                    db_manager.insert_mpe(
                        gmail_id=gmail_id,
                        date=mpe_data.get("date"),
                        supplier=mpe_data.get("supplier"),
                        event=mpe_data.get("event"),
                        mom_link=link_to_mom,
                        key_takeaway=mpe_data.get("key_takeaway"),
                        photos_link=mpe_data.get("photos_link"),
                        region=mpe_data.get("region"),
                        material=mpe_data.get("material")
                    )
                    print(f"\n[STRUCTURED MPE DATA]\n{mpe_data}\n")
            except Exception as e:
                print(f"[ERROR] Failed to extract/insert MPE: {e}")
            
        except Exception as e:
            print(f"[ERROR] Failed to process email {i}: {e}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            continue
    
    print(f"[LOG] Processing complete. Total emails processed: {inserted}")
    return {"inserted": inserted}



def manual_mail_process(subject, body, image_link=None):
    db_manager = DatabaseManager()
    inserted = 0

    # Generate a unique gmail_id using a hash of subject and body
    hash_input = (subject + body).encode('utf-8')
    gmail_id = hashlib.sha256(hash_input).hexdigest()
    sender = "(Manual Entry)"
    received_at = datetime.now(timezone.utc)

    db_manager.insert_email(gmail_id, sender, subject, body, received_at)
    inserted += 1

    # Extract and insert structured data
    print(f"[LOG] Starting extraction for email: {subject[:50]}...")
    
    try:
        print("[LOG] Attempting MoM extraction...")
        mom_data = extract_mom_structured(subject, body)
        if mom_data:
            link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
            db_manager.insert_mom(
                gmail_id=gmail_id,
                date=mom_data.get("date"),
                supplier=mom_data.get("supplier"),
                link_to_mom=link_to_mom,
                key_takeaway=mom_data.get("key_takeaway"),
                region=mom_data.get("region"),
                material=mom_data.get("material")
            )
            print(f"\n[STRUCTURED MOM DATA]\n{mom_data}\n")
        else:
            print("[LOG] No MoM data extracted (email may not be a meeting summary)")
    except Exception as e:
        print(f"[ERROR] Failed to extract/insert MoM: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
    
    try:
        print("[LOG] Attempting JDP extraction...")
        jdp_data = extract_jdp_structured(subject, body)
        if jdp_data:
            link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
            db_manager.insert_jdp(
                gmail_id=gmail_id,
                supplier=jdp_data.get("supplier"),
                project=jdp_data.get("project"),
                mom_link=link_to_mom,
                key_takeaway=jdp_data.get("key_takeaway"),
                next_action_point=jdp_data.get("next_action_point"),
                responsibility=jdp_data.get("responsibility"),
                region=jdp_data.get("region"),
                material=jdp_data.get("material")
            )
            print(f"\n[STRUCTURED JDP DATA]\n{jdp_data}\n")
        else:
            print("[LOG] No JDP data extracted (email may not be a JDP-related email)")
    except Exception as e:
        print(f"[ERROR] Failed to extract/insert JDP: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")

    try:
        print("[LOG] Attempting MPE extraction...")
        mpe_data = extract_mpe_structured(subject, body)
        if mpe_data:
            # Use extracted event if present, otherwise use email content
            event_value = mpe_data.get("event")
            if not event_value or str(event_value).strip() == "":
                event_value = f"Email Subject: {subject} \nEmail Body: {body}"

            link_to_mom = f"Email Subject: {subject} \n Email Body: {body}"
            photos_links = []

            if mpe_data.get("photos_link"):
                photos_links.append(str(mpe_data.get("photos_link")).strip())

            if image_link:
                photos_links += [link.strip() for link in image_link.split(",") if link.strip()]

            photos_links = list(dict.fromkeys(photos_links))

            photos_link_str = ",".join(photos_links) if photos_links else None

            db_manager.insert_mpe(
                gmail_id=gmail_id,
                date=mpe_data.get("date"),
                supplier=mpe_data.get("supplier"),
                event=event_value,
                mom_link=link_to_mom,
                key_takeaway=mpe_data.get("key_takeaway"),
                photos_link=photos_link_str,
                region=mpe_data.get("region"),
                material=mpe_data.get("material")
            )
            print(f"\n[STRUCTURED MPE DATA]\n{mpe_data}\n")
        else:
            print("[LOG] No MPE data extracted (email may not be an MPE event)")
    except Exception as e:
        print(f"[ERROR] Failed to extract/insert MPE: {e}")
        import traceback
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
    
    print(f"[LOG] Manual processing complete. Email inserted: {inserted}")
    return {"inserted": inserted}


def lambda_handler(event=None, context=None):
    # Log event type and keys without printing full content
    if event:
        event_type = type(event).__name__
        if isinstance(event, dict):
            event_keys = list(event.keys())[:5]  # Show first 5 keys
            print(f"Lambda handler invoked: event type={event_type}, keys={event_keys}")
        else:
            print(f"Lambda handler invoked: event type={event_type}")
    else:
        print("Lambda handler invoked: event=None")
    subject = body = None
    image_link = None
    limit = 10  # Default limit for auto processing

    if event:
        # Check if subject and body are directly in event (for direct invocation)
        if isinstance(event, dict) and 'subject' in event and 'body' in event:
            subject = event.get('subject')
            body = event.get('body')
            image_link = event.get('image_link') or event.get('image_urls')
            if isinstance(image_link, list):
                image_link = ','.join(image_link) if image_link else None
        # If event['body'] exists, parse it as JSON to get subject and body (for API Gateway)
        elif 'body' in event:
            try:
                payload = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                subject = payload.get('subject')
                body = payload.get('body')
                image_link = payload.get('image_link') or payload.get('image_urls')
                if isinstance(image_link, list):
                    image_link = ','.join(image_link) if image_link else None
                limit = payload.get('limit', 10)  # Get limit from payload if provided
            except Exception as e:
                print(f"Failed to parse event body: {e}")
        elif isinstance(event, dict):
            # Check if limit is provided directly in event
            limit = event.get('limit', 10)

    if subject and body:
        print(f"Processing email with subject: {subject}")
        return manual_mail_process(subject, body, image_link)
    else:
        print(f"No event data provided, running auto_mail_process with limit={limit}")
        return auto_mail_process(limit=limit)

# For local testing
if __name__ == "__main__":
    # subject = "Quotation Details for Acetic Acid and Glycerine"
    # body = (
    #     "Hi John,\n"
    #     "hope this message finds you well. Please find below the quotation "
    #     "details for the requested chemicals from our vendor, ChemPro "
    #     "Supplies Pvt. Ltd.\n\n"
    #     "1. Acetic Acid 500 L @ $2.50/L\n"
    #     "2. Glycerine 200 kg @ $6.00/kg\n"
    # )
    # manual_mail_process(subject, body)
    event={'subject': 'Minutes of Meeting – Discussion on Glycerine Material with VADILAL CHEMICALS LIMITED', 'body': 'Dear Vendor,\n\nGreetings from [Your Company Name].\n\nPlease find below the Minutes of Meeting held with VADILAL CHEMICALS LIMITED regarding the Glycerine material discussion.\n\n🗓️ Date of Meeting: [Insert Date]\n🕒 Time: [Insert Time]\n📍 Mode: [Online/Offline Meeting Platform or Location]\n👥 Attendees:\n\n[Your Name / Your Team Members] – [Your Company Name]\n\n[Vendor Representative Names] – VADILAL CHEMICALS LIMITED\n\nKey Discussion Points:\n\nDiscussed the current supply status and material availability of Glycerine.\n\nReviewed the latest price trends, market fluctuations, and proposed rate revisions.\n\nVendor shared details on product specifications, batch quality, and certifications (if any).\n\nDiscussion on delivery timelines, lead time, and logistics support.\n\nAddressed pending orders, dispatch schedule, and payment terms.\n\nAgreed to share the updated quotation and quality test reports by [insert due date].\n\nAction Items:\nSl. No.\tAction Item\tResponsible\tTarget Date\n1\tShare updated quotation for Glycerine (including GST & freight)\tVADILAL CHEMICALS LIMITED\t[Date]\n2\tReview internal demand forecast for next quarter\t[Your Company Name]\t[Date]\n3\tConfirm sample testing and feedback\t[Your Company Name]\t[Date]\nNext Steps:\n\nFollow-up meeting to review quotation and finalize procurement terms.\n\nVendor to share batch COA (Certificate of Analysis) and any regulatory documents.\n\nPlease review and confirm if any updates are required.\n\nBest regards,\n', 'image_urls': []}

    lambda_handler(event, context=None)
