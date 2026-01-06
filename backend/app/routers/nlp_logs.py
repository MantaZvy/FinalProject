from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.nlp_log import NlpLogsSchema
from app.models import NlpLogs
from app.db import get_db

router = APIRouter()

# NLP Logs
@router.get("/nlp_logs", response_model=list[NlpLogsSchema])
async def get_nlp_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NlpLogs))
    return result.scalars().all()

@router.post("/nlp_logs", response_model=NlpLogsSchema)
async def add_nlp_log(log: NlpLogsSchema, db: AsyncSession = Depends(get_db)):
    new_log = NlpLogs(**log.dict(exclude_unset=True))
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log