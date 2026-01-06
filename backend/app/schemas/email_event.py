from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class EmailEventsSchema(BaseModel):
    email_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    sender: Optional[str]
    subject: Optional[str]
    snippet: Optional[str]
    detected_status: Optional[str]
    received_at: Optional[datetime.datetime]
    processed_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True