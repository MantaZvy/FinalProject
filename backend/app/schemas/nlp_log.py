from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class NlpLogCreate(BaseModel):
    model_name: Optional[str]
    bleu_score: Optional[float]
    perplexity: Optional[float]
    accuracy: Optional[float]
    notes: Optional[str]

    class Config:
        from_attributes = True
class NlpLogUpdate(BaseModel):
    model_name: Optional[str]
    bleu_score: Optional[float]
    perplexity: Optional[float]
    accuracy: Optional[float]
    notes: Optional[str]

    class Config:
        from_attributes = True
class NlpLogOut(BaseModel):
    run_id: uuid.UUID
    model_name: Optional[str]
    bleu_score: Optional[float]
    perplexity: Optional[float]
    accuracy: Optional[float]
    notes: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True