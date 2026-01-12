from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# Create Schema
class MatchScoreCreate(BaseModel):
    user_id: UUID
    application_id: UUID
    job_id: UUID
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = "skill_overlap_v1"

    model_config = {"from_attributes": True}


# Update Schema
class MatchScoreUpdate(BaseModel):
    similarity_score: Optional[float] = None
    regression_prediction: Optional[float] = None
    model_used: Optional[str] = None

    model_config = {"from_attributes": True}


# Output Schema
class MatchScoreOut(BaseModel):
    score_id: UUID
    user_id: UUID
    application_id: UUID
    job_id: UUID
    similarity_score: Optional[float]
    regression_prediction: Optional[float]
    model_used: Optional[str]
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


# Compute Payload
class MatchScoreCompute(BaseModel):
    user_id: UUID
    application_id: UUID
    job_id: UUID

