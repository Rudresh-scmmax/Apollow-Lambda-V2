import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def main():
    creds = None

    # Load token from JSON
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=8080, prompt='consent')

        # Save the credentials to token.json
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Use Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} messages.")
    for msg in messages:
        print(f"Message ID: {msg['id']}")

if __name__ == '__main__':
    main()



import os
import base64
import psycopg2
from psycopg2.extras import RealDictCursor
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
import google.generativeai as genai

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

# Set Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCJOaGhkqZxQaWSncSuqFp7uvpfs_5iIxE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                port=os.environ.get("DB_PORT"),
                sslmode="require",
                connect_timeout=10
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("Database connection established")
        except psycopg2.OperationalError as e:
            print(f"Database connection error: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected database error: {str(e)}")
            return False
        return True

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def insert_email(self, gmail_id, sender, subject, body, received_at):
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO emails (gmail_id, sender, subject, body, received_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (gmail_id) DO NOTHING
            """, (gmail_id, sender, subject, body, received_at))
            self.conn.commit()
        except Exception as e:
            print(f"[ERROR] Failed to insert email: {e}")
        finally:
            self.disconnect()
        
        def insert_mom(self, gmail_id, date, supplier, link_to_mom, key_takeaway, region):
            print(f"[LOG] Attempting to insert MoM: gmail_id={gmail_id}, date={date}, supplier={supplier}, link_to_mom={link_to_mom}, key_takeaway={key_takeaway}, region={region}")
            try:
                self.connect()
                print("[LOG] Connected to DB, executing insert...")
                self.cursor.execute("""
                    INSERT INTO meeting_minutes (gmail_id, date, supplier, link_to_mom, key_takeaway, region)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (gmail_id) DO NOTHING
                """, (gmail_id, date, supplier, link_to_mom, key_takeaway, region))
                self.conn.commit()
                print("[LOG] Insert committed.")
            except Exception as e:
                print(f"[ERROR] Failed to insert MoM: {e}")
            finally:
                self.disconnect()

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

def extract_mom_structured(subject, body):
    """
    Use Gemini to extract structured MoM data, including region, from the email.
    Returns a dict with keys: date, supplier, link_to_mom, key_takeaway, region.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""
            You are an intelligent assistant extracting structured data from meeting-related emails.  
            Given the email **subject** and **body**, identify if it contains Minutes of Meeting (MoM) content.  
            If yes, extract the following fields and return them in a valid JSON block inside triple backticks (```json ... ```):

            - **date**: Date of the meeting in format "DD MMM YYYY" (e.g., "15 Dec 2024")
            - **supplier**: Name of the company or organization the meeting was with
            - **link_to_mom**: A URL if present in the email body (null if not available)
            - **key_takeaway**: One-sentence summary of the main discussion outcome
            - **region**: Extract the region from the email content (e.g., "India", "Europe", "Japan")

            ### Rules:
            - Only extract if the email is clearly related to a meeting or MoM
            - Do **not guess** values; return null if a field is missing
            - If it's not a meeting email, respond exactly with:  
            **Not a meeting email**

            ---

            **Email Subject**: {subject}

            **Email Body**:
            {body}
            """
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        if "Not a meeting email" in result:
            return None
        import re, json
        match = re.search(r'```json(.*?)```', result, re.DOTALL)
        json_str = match.group(1).strip() if match else result
        mom_data = json.loads(json_str)
        return mom_data
    except Exception as e:
        print(f"[ERROR] Gemini MoM extraction failed: {e}")
        return None

def fetch_and_process_latest_emails(max_results=100):
    db_manager = DatabaseManager()
    service = get_gmail_service()
    messages = []
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages.extend(results.get('messages', []))

    # Optionally, paginate if you want more than max_results
    while 'nextPageToken' in results and len(messages) < max_results:
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results - len(messages),
            pageToken=results['nextPageToken']
        ).execute()
        messages.extend(results.get('messages', []))

    today = datetime.now(timezone.utc).date()
    inserted = 0
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        internal_date = int(msg_data.get('internalDate', 0)) // 1000
        received_at = datetime.fromtimestamp(internal_date, tz=timezone.utc)
        if received_at.date() != today:
            continue  # Only process today's emails

        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        gmail_id = msg['id']
        body = get_email_body(msg_data['payload'])

        db_manager.insert_email(gmail_id, sender, subject, body, received_at)
        inserted += 1

        mom_data = extract_mom_structured(subject, body)
        if mom_data:
            db_manager.insert_mom(
                gmail_id=gmail_id,
                date=mom_data.get("date"),
                supplier=mom_data.get("supplier"),
                link_to_mom=mom_data.get("link_to_mom"),
                key_takeaway=mom_data.get("key_takeaway"),
                region=mom_data.get("region"),
            )
            print(f"\n[STRUCTURED MOM DATA]\n{mom_data}\n")
    return {"inserted": inserted}

# For local testing
if __name__ == '__main__':
    fetch_and_process_latest_emails(max_results=100)