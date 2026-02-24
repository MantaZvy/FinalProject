from googleapiclient.discovery import build
from app.integration.gmail.auth import get_gmail_credentials

def get_gmail_service():
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service