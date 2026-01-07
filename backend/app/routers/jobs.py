from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.job_descriptions import JobDescriptionsCreate, JobDescriptionsUpdate, JobDescriptionsOut
from app.models import JobDescriptions
from app.db import get_db

router = APIRouter(prefix="/jobs",
    tags=["Job Descriptions"])

# Jobs
@router.post("/", response_model=JobDescriptionsOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobDescriptionsCreate,
    db: AsyncSession = Depends(get_db)
):
    job = JobDescriptions(**payload.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

@router.get("/", response_model=list[JobDescriptionsOut])
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobDescriptions))
    return result.scalars().all()

@router.get("/{job_id}", response_model=JobDescriptionsOut)
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(JobDescriptions).where(JobDescriptions.job_id == job_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@router.put("/{job_id}", response_model=JobDescriptionsOut)
async def update_job(
    job_id: str,
    payload: JobDescriptionsUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JobDescriptions).where(JobDescriptions.job_id == job_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    await db.commit()
    await db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(JobDescriptions).where(JobDescriptions.job_id == job_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    await db.delete(job)
    await db.commit()
