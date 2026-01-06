from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class CalendarEventsSchema(BaseModel):
    event_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    event_title: Optional[str]
    event_date: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    google_event_id: Optional[str]

    class Config:
        from_attributes = True