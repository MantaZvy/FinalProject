from app.integration.gmail.service import fetch_application_emails
from app.integration.gmail.parser import detect_application_status

def get_application_status():
    emails = fetch_application_emails()
    applications = []

    for email in emails:
        combined = f"{email['subject']} {email['snippet']}"
        status = detect_application_status(combined)
        if status != "unknown":
            applications.append({
                "email_id": email["id"],
                "from": email["from"],
                "subject": email["subject"],
                "status": status
            })

    return applications