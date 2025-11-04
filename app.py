import torch  # Added for transformers pipeline
from flask import Flask, render_template, request, jsonify, Response
from flask_caching import Cache
from flask_socketio import SocketIO, emit
import sys
import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from transformers import pipeline
import threading
import re
import logging
import json
import time
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dynamic path resolution for src
src_path = r"D:\crm_lead_processing\src"
if os.path.exists(src_path):
    sys.path.insert(0, src_path)
    print("Sys.path:", sys.path)
    print("Using src path:", src_path)
    crm_path = os.path.join(src_path, 'crm.py')
    print("crm.py path:", crm_path)
    print("crm.py exists:", os.path.exists(crm_path))
    try:
        import crm
        print("crm module imported successfully")
        from crm import init_db, add_lead, get_leads
        print("Functions init_db, add_lead, get_leads imported successfully")
    except ImportError as e:
        logger.error("Failed to import from crm: %s", str(e))
else:
    logger.error("src directory not found at %s", src_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-2025'
app.config['CACHE_TYPE'] = 'redis' if os.environ.get('REDIS_URL') else 'simple'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379')
cache = Cache(app, config=app.config)
socketio = SocketIO(app, cors_allowed_origins="*")

# Gmail credentials
EMAIL = "muhammadanshad32575@gmail.com"
PASSWORD = "mouhjhdifouberwx"
IMAP_SERVER = "imap.gmail.com"

# Preload model globally
try:
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli", device=0 if torch.cuda.is_available() else -1, model_kwargs={"torchscript": False}, timeout=30, batch_size=2)
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    classifier = None

# Global cache and lock
emails_cache = {}
lock = threading.Lock()
REFRESH_INTERVAL = 120  # 2 minutes in seconds
MAX_EMAILS = 20  # Limit to 20 emails for performance

def fetch_and_classify_emails(date_filter=None):
    with lock:
        if not classifier:
            return []
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, timeout=10)
            logger.info(f"Attempting login for {EMAIL}")
            mail.login(EMAIL, PASSWORD)
            logger.info("Login successful")
            mail.select("inbox")

            if date_filter:
                if date_filter == "yesterday":
                    target_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
                elif date_filter == "today":
                    target_date = datetime.now().strftime("%d-%b-%Y")
                else:
                    target_date = datetime.strptime(date_filter, "%Y-%m-%d").strftime("%d-%b-%Y")
                logger.info(f"Searching emails SINCE {target_date} for date_filter: {date_filter}")
                status, data = mail.search(None, f'SINCE "{target_date}"')
            else:
                logger.info("Fetching all emails (no date_filter)")
                status, data = mail.search(None, "ALL")

            mail_ids = data[0].split()[:MAX_EMAILS]  # Limit to MAX_EMAILS
            logger.info(f"Found {len(mail_ids)} email IDs")
            emails_data = []
            texts = []
            temp_emails = []

            for num in mail_ids:
                status, msg_data = mail.fetch(num, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_ = msg.get("From")
                content = ""
                attachments = []
                company = "Unknown"

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            content = part.get_payload(decode=True).decode()
                        elif part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is not None:
                            filename = part.get_filename()
                            if filename:
                                attachments.append(filename)
                else:
                    content = msg.get_payload(decode=True).decode()

                name = from_.split("<")[0].strip() if "<" in from_ else "Unknown"
                email_addr = from_.split("<")[1].replace(">", "") if "<" in from_ else from_
                phone = extract_phone(content) or "Not found"
                if "@" in email_addr:
                    company = email_addr.split("@")[1].split(".")[0].capitalize()

                text = str(subject) + " " + (content[:100] if len(content) > 100 else content)
                texts.append(text)
                temp_emails.append({
                    "name": name,
                    "email": email_addr,
                    "phone": phone,
                    "content": content[:200] + "..." if len(content) > 200 else content,
                    "company": company,
                    "message_link": f"https://mail.google.com/mail/u/0/#search/{subject.replace(' ', '+')}",
                    "attachments": attachments if attachments else None
                })

            if texts:
                if classifier:
                    candidate_labels = ["Lead", "Support", "Spam", "Follow-up"]
                    results = classifier(texts, candidate_labels, multi_label=False)
                    for result, temp in zip(results, temp_emails):
                        temp["classification"] = result['labels'][0]
                        emails_data.append(temp)
                else:
                    for temp in temp_emails:
                        temp["classification"] = "Unclassified"
                        emails_data.append(temp)

            mail.logout()
            logger.info(f"Fetched {len(emails_data)} emails")
            return emails_data
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []

def get_cached_emails(date_filter=None):
    # Bypass cache key generation issue in threads by using a static key
    cache_key = f"emails_{date_filter or 'all'}"
    rv = cache.get(cache_key)
    if rv is None:
        rv = fetch_and_classify_emails(date_filter)
        cache.set(cache_key, rv, timeout=120)
    return rv

def extract_phone(text):
    phone = re.search(r'\b\d{10}\b|\+\d{10,12}', text)
    return phone.group(0) if phone else None

def authenticate_user():
    return True  # Placeholder

# Initialize database at startup
init_db("db/crm.db")

# Background task to fetch and update emails
def load_initial_emails():
    time.sleep(1) # Short delay
    socketio.emit('update', {'emails': get_cached_emails(), 'current_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")})

@socketio.on('connect')
def handle_connect():
    if not authenticate_user():
        emit('error', {'message': 'Authentication failed'})
        return False
    logger.info("Client connected")
    threading.Thread(target=load_initial_emails, daemon=True).start()

@socketio.on('filter_date')
def handle_filter_date(date_filter):
    if authenticate_user():
        emails_data = get_cached_emails(date_filter)
        emit('update', {'emails': emails_data, 'current_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")}, broadcast=True)

def background_task(date_filter="today"):
    time.sleep(5) # Delay to avoid contention
    while True:
        try:
            if authenticate_user():
                logger.info(f"Background task running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
                emails_data = fetch_and_classify_emails(date_filter)
                with lock:
                    conn = sqlite3.connect("db/crm.db")
                    c = conn.cursor()
                    c.executemany("INSERT OR IGNORE INTO leads (name, email, phone, classification, date) VALUES (?, ?, ?, ?, ?)", 
                                  [(email["name"], email["email"], email["phone"], email["classification"], datetime.now().strftime("%Y-%m-%d")) for email in emails_data])
                    conn.commit()
                    conn.close()
                logger.info(f"Emitting update with {len(emails_data)} emails")
                socketio.emit('update', {'emails': emails_data, 'current_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")})
        except Exception as e:
            logger.error(f"Error in background task: {e}")
        time.sleep(REFRESH_INTERVAL) # Use time.sleep instead of Event.wait

@app.route("/", methods=["GET", "POST"])
def home():
    if not authenticate_user():
        return "Unauthorized", 401
    date_filter = request.args.get("date_filter", "today")
    # Return initial response quickly with loading state
    return render_template("dashboard.html", emails=[], current_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"), date_filter=date_filter, loading=True)

@app.route("/api/filter", methods=["POST"])
def filter_emails():
    if not authenticate_user():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    date_filter = data.get("date_filter", "today")
    emails_data = get_cached_emails(date_filter)
    return jsonify({"emails": emails_data, "current_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")})

if __name__ == "__main__":
    threading.Thread(target=background_task, args=("today",), daemon=True).start()
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)