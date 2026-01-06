from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.calendar_event import CalendarEventsSchema
from app.models import CalendarEvents
from app.db import get_db

router = APIRouter()

# Calendar Events
@router.get("/calendar_events", response_model=list[CalendarEventsSchema])
async def get_calendar_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CalendarEvents))
    return result.scalars().all()

@router.post("/calendar_events", response_model=CalendarEventsSchema)
async def add_calendar_event(event: CalendarEventsSchema, db: AsyncSession = Depends(get_db)):
    new_event = CalendarEvents(**event.dict(exclude_unset=True))
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event