from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.job_seeker import JobSeekerSchema
from models import JobSeeker
from db import get_db

router = APIRouter()

# Job Seekers
@router.get("/job_seekers", response_model=list[JobSeekerSchema])
async def get_job_seekers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobSeeker))
    return result.scalars().all()

@router.post("/job_seekers", response_model=JobSeekerSchema)
async def add_job_seeker(user: JobSeekerSchema, db: AsyncSession = Depends(get_db)):
    new_user = JobSeeker(**user.dict(exclude_unset=True))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user