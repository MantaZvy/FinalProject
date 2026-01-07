from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class CalendarEventCreate(BaseModel):
    application_id: uuid.UUID
    event_title: str
    event_date: datetime
    google_event_id: Optional[str]


class CalendarEventUpdate(BaseModel):
    event_title: Optional[str]
    event_date: Optional[datetime.datetime]
    google_event_id: Optional[str]


class CalendarEventOut(BaseModel):
    event_id: uuid.UUID
    application_id: uuid.UUID
    event_title: str
    event_date: datetime
    google_event_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
