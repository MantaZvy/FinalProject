from app.integration.gmail.service import fetch_application_emails
from app.integration.gmail.parser import detect_application_status
from app.models import Applications, EmailEvents
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4

STATUS_PRIORITY = {
    "applied": 1,
    "interview": 2,
    "offer": 3
}

TERMINAL_STATUSES = {"rejected"}

def should_update_status(current_status: str | None, new_status: str) -> bool:
    if new_status == "unknown":
        return False

    if new_status in TERMINAL_STATUSES:
        return True

    if current_status in TERMINAL_STATUSES:
        return False

    if not current_status:
        return True

    current_rank = STATUS_PRIORITY.get(current_status, 0)
    new_rank = STATUS_PRIORITY.get(new_status, 0)

    return new_rank > current_rank

def extract_domain(sender: str | None) -> str | None:
    if not sender or "@" not in sender:
        return None
    return sender.split("@")[-1].lower()

def find_application_by_email(session: Session, user_id, sender: str, subject:str):
    domain = extract_domain(sender)
    applications = session.query(Applications).filter(
        Applications.user_id == user_id
    ).all()
    
    if domain:#domain matching is more reliable than subject matching, so we prioritize
        for app in applications:
            if app.company and domain in app.company.lower():
                return app
    
    for app in applications:#company in subject (email) to see if matching failed
        if app.company and app.company.lower() in subject.lower():
            return app
    for app in applications:#job title in subject see if matching failed 
        if app.job_title and app.job_title.lower() in subject.lower():
            return app
    return None

def sync_gmail_applications(session: Session, user_id):
    emails = fetch_application_emails()
    for email in emails:
        #duplication check
        existing = session.query(EmailEvents).filter_by(
            gmail_message_id=email["id"]
        ).first()
        if existing:
            continue
        status = detect_application_status(
            email["subject"],
            email["snippet"]
        )
        linked_application = find_application_by_email(
            session=session,
            user_id=user_id,
            sender=email["from"],
            subject=email["subject"]
        )
        email_event = EmailEvents(
            id=uuid4(),
            gmail_message_id=email["id"],
            sender=email["from"],
            subject=email["subject"],
            snippet=email["snippet"],
            detected_status=status,
            received_at=datetime.utcnow(),
            application_id=linked_application.application_id if linked_application else None
        )
        session.add(email_event)

        if linked_application and should_update_status(
            linked_application.status,
            status
        ):
            linked_application.status = status
    session.commit()

