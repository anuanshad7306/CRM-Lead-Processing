import imaplib
import email
import os
import yaml

def fetch_emails():
    with open("config/settings.yaml") as f:
        settings = yaml.safe_load(f)
    imap_server = settings["email"]["imap_server"]
    username = settings["email"]["username"]
    password = settings["email"]["password"]

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    ids = data[0].split()
    for num in ids[-10:]:  # Fetch last 10 emails
        result, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        with open(f"data/fetched_emails/{num.decode()}.eml", "wb") as f:
            f.write(raw_email)

    mail.close()
    mail.logout()