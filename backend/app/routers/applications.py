from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationOut
from app.models import Applications, JobDescriptions, JobSeeker
from app.db import get_db

router = APIRouter(prefix="/applications", tags=["Applications"])

# Applications
#Create Application
@router.post("/", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
async def create_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db)
):
    # validate JobSeeker
    user = await db.scalar(
        select(JobSeeker).where(JobSeeker.user_id == payload.user_id)
    )
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # validate JobDescription
    job = await db.scalar(
        select(JobDescriptions).where(JobDescriptions.job_id == payload.job_id)
    )
    if not job:
        raise HTTPException(status_code=400, detail="Invalid job_id")

    application = Applications(**payload.model_dump())
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application

#Get All
@router.get("/", response_model=list[ApplicationOut])
async def get_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Applications))
    return result.scalars().all()

#Get by ID
@router.get("/{application_id}", response_model=ApplicationOut)
async def get_application(application_id: str, db: AsyncSession = Depends(get_db)):
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application

#Update
@router.put("/{application_id}", response_model=ApplicationOut)
async def update_application(
    application_id: str,
    payload: ApplicationUpdate,
    db: AsyncSession = Depends(get_db)
):
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(application, field, value)

    await db.commit()
    await db.refresh(application)
    return application

#Delete
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id: str, db: AsyncSession = Depends(get_db)):
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    await db.delete(application)
    await db.commit()
