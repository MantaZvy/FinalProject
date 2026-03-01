from googleapiclient.discovery import build
from app.integration.gmail.auth import get_gmail_credentials
from typing import List, Dict, Any
from app.integration.gmail.parser import detect_application_status



def get_gmail_service():
    creds = get_gmail_credentials()
    return build("gmail", "v1", credentials=creds)


def fetch_application_emails(max_results: int = 10) -> List[Dict[str, Any]]:
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q="newer_than:7d",#working only with recent emails to avoid irrelavent fetching
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = msg_data.get("payload", {}).get("headers", [])

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "From":
                sender = h["value"]

        snippet = msg_data.get("snippet", "")
        status = detect_application_status(subject, snippet)

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "from": sender,
            "snippet": snippet,
            "status": status
        })

    return emails