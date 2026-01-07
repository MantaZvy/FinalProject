from pydantic import BaseModel
from typing import Optional, List
import uuid, datetime

class JobSeekerCreate(BaseModel):
    profile_summary: Optional[str]
    skills: Optional[List[str]]
    education: Optional[dict]
    experience: Optional[dict]
    certifications: Optional[List[str]]
    keywords: Optional[List[str]]


class JobSeekerUpdate(BaseModel):
    profile_summary: Optional[str] = None
    skills: Optional[List[str]] = None
    education: Optional[dict] = None
    experience: Optional[dict] = None
    certifications: Optional[List[str]] = None
    keywords: Optional[List[str]] = None


class JobSeekerOut(BaseModel):
    user_id: Optional[uuid.UUID]
    profile_summary: Optional[str]
    skills: Optional[List[str]]
    education: Optional[dict]
    experience: Optional[dict]
    certifications: Optional[List[str]]
    keywords: Optional[List[str]]
    created_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True