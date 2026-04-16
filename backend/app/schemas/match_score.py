from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
import uuid, datetime

# Create Schema
class MatchScoreCreate(BaseModel):
    user_id: UUID
    application_id: UUID
    job_id: UUID
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = "skill_overlap_v1"

    model_config = {"from_attributes": True}
class MatchScoreUpdate(BaseModel):
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = None

    model_config = {"from_attributes": True}
class MatchScoreOut(BaseModel):
    score_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    application_id: Optional[uuid.UUID] = None 
    job_id: Optional[uuid.UUID] = None
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = None
    matched_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    explanation: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    recommendations: Optional[Any] = None

    class Config:
        from_attributes = True
class MatchScoreCompute(BaseModel):#compute payload
    user_id: UUID
    application_id: UUID
    job_id: UUID

