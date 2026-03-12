from datetime import datetime
from app.integration.calendar.service import create_interview_event

create_interview_event(
    "Test Interview – Backend Engineer",
    datetime.utcnow()
)