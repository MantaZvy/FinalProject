from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.email_event import EmailEventsSchema
from app.models import EmailEvents
from app.db import get_db

router = APIRouter()

# Email Events
@router.get("/email_events", response_model=list[EmailEventsSchema])
async def get_email_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailEvents))
    return result.scalars().all()

@router.post("/email_events", response_model=EmailEventsSchema)
async def add_email_event(email: EmailEventsSchema, db: AsyncSession = Depends(get_db)):
    new_email = EmailEvents(**email.dict(exclude_unset=True))
    db.add(new_email)
    await db.commit()
    await db.refresh(new_email)
    return new_email