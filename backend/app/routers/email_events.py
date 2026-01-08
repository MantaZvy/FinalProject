from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.email_event import EmailEventCreate, EmailEventUpdate, EmailEventOut
from app.models import EmailEvents, Applications
from app.db import get_db
import uuid

router = APIRouter(prefix="/email_events", tags=["Email Events"])

# Email Event
#Create
@router.post("/", response_model=EmailEventOut, status_code=status.HTTP_201_CREATED)
async def create_email_event(
    payload: EmailEventCreate,
    db: AsyncSession = Depends(get_db)
):
    #validate application id
    application = await db.scalar(
        select(Applications).where(Applications.application_id == payload.application_id)
    )
    if not application:
        raise HTTPException(status_code=400, detail="Invalid application_id")

    event = EmailEvents(**payload.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

#Read all
@router.get("/", response_model=list[EmailEventOut])
async def get_email_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailEvents))
    return result.scalars().all()

#Read by ID
@router.get("/{email_id}", response_model=EmailEventOut)
async def get_email_event(email_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    event = await db.scalar(
        select(EmailEvents).where(EmailEvents.email_id == email_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Email event not found")
    return event

#Update
@router.put("/{email_id}", response_model=EmailEventOut)
async def update_email_event(
    email_id: uuid.UUID,
    payload: EmailEventUpdate,
    db: AsyncSession = Depends(get_db)
):
    event = await db.scalar(
        select(EmailEvents).where(EmailEvents.email_id == email_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Email event not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    await db.commit()
    await db.refresh(event)
    return event

#Delete
@router.delete("/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email_event(email_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    event = await db.scalar(
        select(EmailEvents).where(EmailEvents.email_id == email_id)
    )
    if not event:
        raise HTTPException(status_code=404, detail="Email event not found")

    await db.delete(event)
    await db.commit()