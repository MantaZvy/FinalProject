from app.integration.gmail.service import fetch_application_emails
from app.integration.gmail.parser import detect_application_status, extract_interview_datetime, extract_meeting_link
from app.integration.calendar.service import create_interview_event
from app.models import Applications, EmailEvents
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
import asyncio

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

async def find_application_by_email(session: AsyncSession, user_id, sender: str, subject:str):
    domain = extract_domain(sender)
    result = await session.execute(
        select(Applications).where(
            Applications.user_id == user_id
        )
    )

    applications = result.scalars().all()
    
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

async def sync_gmail_applications(session: AsyncSession, user_id):
    emails = fetch_application_emails()
    for email in emails:
        #duplication check
        result = await session.execute(
            select(EmailEvents).where(
                EmailEvents.gmail_message_id == email["id"]
                )
            )
        existing = result.scalar_one_or_none()
        if existing:
            continue
        content = f" {email['subject']} {email['snippet']} {email['body']}"
        status = detect_application_status(email["subject"], f"{email['snippet']} {email['body']}")
        interview_date = extract_interview_datetime(content)
        meeting_link = extract_meeting_link(content)
        linked_application = await find_application_by_email(
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
            meeting_link=meeting_link,
            application_id=linked_application.application_id if linked_application else None
        )
        session.add(email_event)

        if linked_application:
            if should_update_status(linked_application.status, status):#if new interview date, update status
                linked_application.status = status#store status in db
            if interview_date and not linked_application.interview_date:#update if we don't have an interview date
                linked_application.interview_date = interview_date
                await asyncio.to_thread(#wrap asynchrynous to env so woulnd't block main thread
                    create_interview_event,#if there's an interview date, create calendar event
                    title=f"Interview - {linked_application.job_title} @ {linked_application.company}",
                    interview_date=interview_date,
                    meeting_link=meeting_link
                )
            if meeting_link:#update if don't have meeting link
                linked_application.meeting_link = meeting_link
            
            
    await session.commit()

