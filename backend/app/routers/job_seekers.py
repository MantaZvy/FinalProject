import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_seeker import JobSeekerSchema
from app.models import JobSeeker
from app.db import get_db

router = APIRouter()

# Job Seekers
@router.get("/job_seekers", response_model=list[JobSeekerSchema])
async def get_job_seekers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobSeeker))
    return result.scalars().all()
#Add job seeker
@router.post("/job_seekers", response_model=JobSeekerSchema)
async def add_job_seeker(user: JobSeekerSchema, db: AsyncSession = Depends(get_db)):
    new_user = JobSeeker(**user.dict(exclude_unset=True))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# GET a single job seeker by user_id
@router.get("/job_seekers/{user_id}", response_model=JobSeekerSchema)
async def get_job_seeker(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        uid = uuid.UUID(user_id)  # validate UUID format
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid UUID format") from exc
    
    result = await db.execute(select(JobSeeker).where(JobSeeker.user_id == uid))
    job_seeker = result.scalar_one_or_none()

    if not job_seeker:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    
    return job_seeker