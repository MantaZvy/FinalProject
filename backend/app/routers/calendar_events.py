from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.calendar_event import CalendarEventCreate, CalendarEventUpdate, CalendarEventOut
from app.models import CalendarEvents, Applications
from app.db import get_db

router = APIRouter(prefix="/calendar-events", tags=["Calendar Events"])

# Calendar Events
#Create
@router.post(
    "/", 
    response_model=CalendarEventOut, 
    status_code=status.HTTP_201_CREATED
)
async def create_calendar_event(
    payload: CalendarEventCreate,
    db: AsyncSession = Depends(get_db)
):
    application = await db.scalar(
        select(Applications).where(
            Applications.application_id == payload.application_id
        )
    )
    if not application:
        raise HTTPException(status_code=400, detail="Invalid application_id")

    event = CalendarEvents(**payload.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


#Read all
@router.get("/", response_model=list[CalendarEventOut])
async def get_calendar_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CalendarEvents))
    return result.scalars().all()

#Read by ID
@router.get("/{event_id}", response_model=CalendarEventOut)
async def get_calendar_event(event_id: str, db: AsyncSession = Depends(get_db)):
    event = await db.scalar(
        select(CalendarEvents).where(CalendarEvents.event_id == event_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Calendar event not found")

    return event

#Update
@router.put("/{event_id}", response_model=CalendarEventOut)
async def update_calendar_event(
    event_id: str,
    payload: CalendarEventUpdate,
    db: AsyncSession = Depends(get_db)
):
    event = await db.scalar(
        select(CalendarEvents).where(CalendarEvents.event_id == event_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Calendar event not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    await db.commit()
    await db.refresh(event)
    return event

#Delete
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_event(event_id: str, db: AsyncSession = Depends(get_db)):
    event = await db.scalar(
        select(CalendarEvents).where(CalendarEvents.event_id == event_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Calendar event not found")

    await db.delete(event)
    await db.commit()
