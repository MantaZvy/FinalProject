from pydantic import BaseModel
from typing import Optional, List
import uuid, datetime

class JobDescriptionsCreate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None


class JobDescriptionsUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None


class JobDescriptionsOut(BaseModel):
    job_id: Optional[uuid.UUID]
    title: Optional[str]
    company: Optional[str]
    description: Optional[str]
    skills_required: Optional[List[str]]
    keywords: Optional[List[str]]
    source: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True