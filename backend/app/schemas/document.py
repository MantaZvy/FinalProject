from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class DocumentsSchema(BaseModel):
    document_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    doc_type: Optional[str]
    content: Optional[str]
    file_path: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True