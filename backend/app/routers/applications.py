from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.application import ApplicationsSchema
from app.models import Applications
from app.db import get_db

router = APIRouter()

# Applications
@router.get("/applications", response_model=list[ApplicationsSchema])
async def get_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Applications))
    return result.scalars().all()

@router.post("/applications", response_model=ApplicationsSchema)
async def add_application(application: ApplicationsSchema, db: AsyncSession = Depends(get_db)):
    new_app = Applications(**application.dict(exclude_unset=True))
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app