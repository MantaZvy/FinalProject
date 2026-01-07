from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class DocumentCreate(BaseModel):
    user_id: uuid.UUID
    doc_type: str
    content: Optional[str]
    file_path: Optional[str]

class DocumentUpdate(BaseModel):
    doc_type: Optional[str]
    content: Optional[str]
    file_path: Optional[str]

class DocumentOut(BaseModel):
    document_id: uuid.UUID
    user_id: uuid.UUID
    doc_type: str
    content: Optional[str]
    file_path: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True