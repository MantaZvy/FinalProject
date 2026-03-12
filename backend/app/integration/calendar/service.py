from googleapiclient.discovery import build
from app.integration.gmail.auth import get_gmail_credentials
from datetime import timedelta


def get_calendar_service():
    creds = get_gmail_credentials()
    return build("calendar", "v3", credentials=creds)

def create_interview_event(title, interview_date, meeting_link=None):
    service = get_calendar_service()

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