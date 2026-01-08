from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.nlp_log import NlpLogCreate, NlpLogOut, NlpLogUpdate
from app.models import NlpLogs
from app.db import get_db

router = APIRouter(prefix="/nlp_logs", tags=["NLP Logs"])

# NLP Logs
#Create
@router.post("/", response_model=NlpLogOut, status_code=status.HTTP_201_CREATED)
async def create_nlp_log(payload: NlpLogCreate, db: AsyncSession = Depends(get_db)):
    log = NlpLogs(**payload.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

#Read all
@router.get("/", response_model=list[NlpLogOut])
async def get_nlp_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NlpLogs))
    return result.scalars().all()

#Read by ID
@router.get("/{run_id}", response_model=NlpLogOut)
async def get_nlp_log(run_id: str, db: AsyncSession = Depends(get_db)):
    log = await db.scalar(select(NlpLogs).where(NlpLogs.run_id == run_id))
    if not log:
        raise HTTPException(status_code=404, detail="NLP log not found")
    return log

#Update
@router.put("/{run_id}", response_model=NlpLogOut)
async def update_nlp_log(run_id: str, payload: NlpLogUpdate, db: AsyncSession = Depends(get_db)):
    log = await db.scalar(select(NlpLogs).where(NlpLogs.run_id == run_id))
    if not log:
        raise HTTPException(status_code=404, detail="NLP log not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(log, field, value)

    await db.commit()
    await db.refresh(log)
    return log

#Delete
@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nlp_log(run_id: str, db: AsyncSession = Depends(get_db)):
    log = await db.scalar(select(NlpLogs).where(NlpLogs.run_id == run_id))
    if not log:
        raise HTTPException(status_code=404, detail="NLP log not found")

    await db.delete(log)
    await db.commit()