from pydantic import BaseModel
import uuid


class ResumeParseResponse(BaseModel):
    document_id: uuid.UUID
    user_id: uuid.UUID
    extracted_text: str
    model_name: str

    class Config:
        from_attributes = True

