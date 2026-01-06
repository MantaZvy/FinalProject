from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_descriptions import JobDescriptionsSchema
from app.models import JobDescriptions
from app.db import get_db

router = APIRouter()

# Jobs
@router.get("/jobs", response_model=list[JobDescriptionsSchema])
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobDescriptions))
    return result.scalars().all()

@router.post("/jobs", response_model=JobDescriptionsSchema)
async def add_job(job: JobDescriptionsSchema, db: AsyncSession = Depends(get_db)):
    new_job = JobDescriptions(**job.dict(exclude_unset=True))
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job