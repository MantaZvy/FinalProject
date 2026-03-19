from googleapiclient.discovery import build
from app.integration.gmail.auth import get_gmail_credentials
from datetime import timedelta, timezone 

_calendar_service = None #catch only once per build to avoid multiple auth calls/charges

def get_calendar_service():
    global _calendar_service
    if _calendar_service is None:
        creds = get_gmail_credentials()
        _calendar_service = build("calendar", "v3", credentials=creds)
    return _calendar_service

def create_interview_event(title, interview_date, meeting_link=None):
    service = get_calendar_service()
    if interview_date.tzinfo is None:#timezone aware ISO format
        interview_date = interview_date.replace(tzinfo=timezone.utc)
    event = {
        "summary": title,
        "description": f"Interview scheduled automatically.\n{meeting_link or ''}",
        "start": {
            "dateTime": interview_date.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": (interview_date + timedelta(hours=1)).isoformat(),
            "timeZone": "UTC"
        }
    }

    event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return event["id"]