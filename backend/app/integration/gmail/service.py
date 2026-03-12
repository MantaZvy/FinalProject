from googleapiclient.discovery import build
from app.integration.gmail.auth import get_gmail_credentials
from typing import List, Dict, Any
from app.integration.gmail.parser import detect_application_status
import base64 #converts from binary to text format data



def get_gmail_service():
    creds = get_gmail_credentials()
    return build("gmail", "v1", credentials=creds)

def extract_email_body(payload):
    if "parts" in payload:#multipart email rendering to find plain text
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    decoded = base64.urlsafe_b64decode(data)
                    return decoded.decode("utf-8", errors="ignore")

    body_data = payload.get("body", {}).get("data")#if not multiplart, try get full body data

    if body_data:
        decoded = base64.urlsafe_b64decode(body_data)
        return decoded.decode("utf-8", errors="ignore")

    return ""

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

        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        body = extract_email_body(payload)

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "From":
                sender = h["value"]

        snippet = msg_data.get("snippet", "")
        status = detect_application_status(content=f"{subject} {snippet} {body}")

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "from": sender,
            "snippet": snippet,
            "body": body,
            "status": status
        })

    return emails