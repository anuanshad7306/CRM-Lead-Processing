import sqlite3
import os
from datetime import datetime

def init_db(db_path="db/crm.db"):
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path) or "."
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads
                 (name TEXT, email TEXT, phone TEXT, classification TEXT, date TEXT)''')
    # Sample data for testing
    sample_data = [
        ("John Doe", "john@example.com", "1234567890", "Lead", "2025-10-01"),
        ("Jane Smith", "jane@example.com", "9876543210", "Support", "2025-10-02"),
        ("Bob Johnson", "bob@example.com", "5555555555", "Lead", "2025-10-03"),
        ("Alice Brown", "alice@example.com", "4444444444", "Follow-up", "2025-10-04"),
        ("Mike Wilson", "mike@example.com", "3333333333", "Spam", "2025-10-05"),
        ("Sarah Davis", "sarah@example.com", "2222222222", "Lead", "2025-10-06"),
        ("Tom Lee", "tom@example.com", "1111111111", "Support", "2025-10-07")
    ]
    c.executemany("INSERT OR IGNORE INTO leads (name, email, phone, classification, date) VALUES (?, ?, ?, ?, ?)", sample_data)
    
    conn.commit()
    conn.close()

def add_lead(name, email, phone, classification, db_path="db/crm.db"):
    db_dir = os.path.dirname(db_path) or "."
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, email, phone, classification, date) VALUES (?, ?, ?, ?, ?)",
              (name, email, phone, classification, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_leads(db_path="db/crm.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT date FROM leads")
    leads = c.fetchall()
    conn.close()
    return leads