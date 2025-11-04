import re

def extract_lead(email_text):
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email_text)
    phone_match = re.search(r"\b\d{10}\b", email_text)
    name_match = re.search(r"My name is (\w+ \w+)", email_text)
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "name": name_match.group(1) if name_match else None
    }