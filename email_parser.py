import email

def parse_email(file_path):
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f)
    subject = msg["subject"]
    from_addr = msg["from"]
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
    return {"subject": subject, "from": from_addr, "body": body}