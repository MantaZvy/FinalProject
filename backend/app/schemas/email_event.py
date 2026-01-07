from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class EmailEventCreate(BaseModel):
    application_id: uuid.UUID
    sender: Optional[str]
    subject: Optional[str]
    snippet: Optional[str]
    detected_status: Optional[str]
    received_at: Optional[datetime.datetime]

class EmailEventUpdate(BaseModel):
    sender: Optional[str]
    subject: Optional[str]
    snippet: Optional[str]
    detected_status: Optional[str]
    received_at: Optional[datetime.datetime]

class EmailEventOut(BaseModel):
    email_id: uuid.UUID
    application_id: uuid.UUID
    sender: Optional[str]
    subject: Optional[str]
    snippet: Optional[str]
    detected_status: Optional[str]
    received_at: Optional[datetime.datetime]
    processed_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True