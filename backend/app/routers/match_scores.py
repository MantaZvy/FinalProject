from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.match_score import MatchScoresSchema
from models import MatchScores
from db import get_db

router = APIRouter()

# Match Scores
@router.get("/match_scores", response_model=list[MatchScoresSchema])
async def get_match_scores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MatchScores))
    return result.scalars().all()

@router.post("/match_scores", response_model=MatchScoresSchema)
async def add_match_score(score: MatchScoresSchema, db: AsyncSession = Depends(get_db)):
    new_score = MatchScores(**score.dict(exclude_unset=True))
    db.add(new_score)
    await db.commit()
    await db.refresh(new_score)
    return new_score