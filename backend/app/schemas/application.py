from pydantic import BaseModel
from typing import Optional
import uuid, datetime

class ApplicationCreate(BaseModel):
    user_id: Optional[uuid.UUID]
    job_id: Optional[uuid.UUID]
    job_title: Optional[str]
    company: Optional[str]
    platform: Optional[str]
    status: Optional[str]
    salary_range: Optional[str]
    notes: Optional[str]
    applied_date: Optional[datetime.date]


class ApplicationUpdate(BaseModel):
    job_title: Optional[str]
    company: Optional[str]
    platform: Optional[str]
    status: Optional[str]
    salary_range: Optional[str]
    notes: Optional[str]
    applied_date: Optional[datetime.date]


class ApplicationOut(BaseModel):
    application_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    job_id: Optional[uuid.UUID]
    job_title: Optional[str]
    company: Optional[str]
    platform: Optional[str]
    status: Optional[str]
    salary_range: Optional[str]
    notes: Optional[str]
    applied_date: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True