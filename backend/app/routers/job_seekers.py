import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_seeker import JobSeekerCreate, JobSeekerUpdate, JobSeekerOut 
from app.models import JobSeeker
from app.db import get_db

router = APIRouter(prefix="/job_seekers", tags=["Job Seekers"])

# Job Seekers
@router.post("", response_model=JobSeekerOut)
async def create_job_seeker(
    payload: JobSeekerCreate,
    db: AsyncSession = Depends(get_db)
):
    job_seeker = JobSeeker(**payload.model_dump(exclude_unset=True))
    db.add(job_seeker)
    await db.commit()
    await db.refresh(job_seeker)
    return job_seeker


@router.get("", response_model=list[JobSeekerOut])
async def get_all_job_seekers(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(JobSeeker))
    return result.scalars().all()


@router.get("/{user_id}", response_model=JobSeekerOut)
async def get_job_seeker(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JobSeeker).where(JobSeeker.user_id == user_id)
    )
    job_seeker = result.scalar_one_or_none()

    if not job_seeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")

    return job_seeker


@router.put("/{user_id}", response_model=JobSeekerOut)
async def update_job_seeker(
    user_id: uuid.UUID,
    payload: JobSeekerUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JobSeeker).where(JobSeeker.user_id == user_id)
    )
    job_seeker = result.scalar_one_or_none()

    if not job_seeker:
        raise HTTPException(status_code=404, detail="JobSeeker not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job_seeker, field, value)

    await db.commit()
    await db.refresh(job_seeker)
    return job_seeker