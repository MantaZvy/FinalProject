from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class MatchScoresSchema(BaseModel):
    score_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    job_id: Optional[uuid.UUID]
    similarity_score: Optional[float]
    regression_prediction: Optional[float]
    model_used: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True