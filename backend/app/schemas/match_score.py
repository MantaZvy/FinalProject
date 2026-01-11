from pydantic import BaseModel
from typing import Optional
import uuid, datetime
class MatchScoreCreate(BaseModel):
    user_id: uuid.UUID
    application_id: uuid.UUID
    job_id: uuid.UUID
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = "skill_overlap_v1"

    class Config:
        from_attributes = True

# Update Schema
class MatchScoreUpdate(BaseModel):
    similarity_score: Optional[float]
    regression_prediction: Optional[float]
    model_used: Optional[str]

    class Config:
        from_attributes = True

# Output Schema
class MatchScoreOut(BaseModel):
    score_id: uuid.UUID
    user_id: uuid.UUID
    application_id: uuid.UUID
    job_id: uuid.UUID
    similarity_score: Optional[float]
    regression_prediction: Optional[float]
    model_used: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True