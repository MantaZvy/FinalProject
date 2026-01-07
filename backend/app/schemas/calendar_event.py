from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class CalendarEventCreate(BaseModel):
    application_id: uuid.UUID
    event_title: str
    event_date: datetime
    google_event_id: Optional[str] = None


class CalendarEventUpdate(BaseModel):
    event_title: Optional[str] = None
    event_date: Optional[datetime] = None
    google_event_id: Optional[str] = None


class CalendarEventOut(BaseModel):
    event_id: uuid.UUID
    application_id: uuid.UUID
    event_title: str
    event_date: datetime
    google_event_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
