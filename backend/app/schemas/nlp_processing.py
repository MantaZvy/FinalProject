from pydantic import BaseModel
from typing import Optional, Dict
import uuid
import datetime


class ResumeParseResponse(BaseModel):
    document_id: uuid.UUID
    user_id: uuid.UUID
    extracted_text: str
    model_name: str

    # Structured fields from parsed resume
    parsed_resume: Optional[Dict[str, Optional[object]]] = None

    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
