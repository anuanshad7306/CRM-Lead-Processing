import os
from src import email_fetcher, email_parser, lead_extractor, crm

def process_emails():
    crm.init_db()
    for filename in os.listdir("data/fetched_emails"):
        if filename.endswith(".eml"):
            email_data = email_parser.parse_email(f"data/fetched_emails/{filename}")
            lead = lead_extractor.extract_lead(email_data["body"])
            crm.add_lead(lead.get("name"), lead.get("email"), lead.get("phone"), email_data["from"])
    print("Processed emails and updated CRM.")

if __name__ == "__main__":
    process_emails()