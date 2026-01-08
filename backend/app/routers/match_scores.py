from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.match_score import MatchScoreCreate, MatchScoreUpdate, MatchScoreOut
from app.models import MatchScores, Applications, JobDescriptions, JobSeeker    
from app.db import get_db
import uuid

router = APIRouter(prefix="/match_scores", tags=["Match Scores"])

# Match Scores
#Create
@router.post("/", response_model=MatchScoreOut, status_code=status.HTTP_201_CREATED)
async def create_match_score(
    payload: MatchScoreCreate,
    db: AsyncSession = Depends(get_db)
):
    # Validate related records exist
    application = await db.scalar(select(Applications).where(Applications.application_id == payload.application_id))
    if not application:
        raise HTTPException(status_code=400, detail="Invalid application_id")
    
    job = await db.scalar(select(JobDescriptions).where(JobDescriptions.job_id == payload.job_id))
    if not job:
        raise HTTPException(status_code=400, detail="Invalid job_id")
    
    user = await db.scalar(select(JobSeeker).where(JobSeeker.user_id == payload.user_id))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    score = MatchScores(**payload.model_dump())
    db.add(score)
    await db.commit()
    await db.refresh(score)
    return score

#Read all
@router.get("/", response_model=list[MatchScoreOut])
async def get_match_scores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MatchScores))
    return result.scalars().all()

#Read by ID
@router.get("/{score_id}", response_model=MatchScoreOut)
async def get_match_score(score_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    score = await db.scalar(select(MatchScores).where(MatchScores.score_id == score_id))
    if not score:
        raise HTTPException(status_code=404, detail="Match score not found")
    return score

#Update
@router.put("/{score_id}", response_model=MatchScoreOut)
async def update_match_score(
    score_id: uuid.UUID,
    payload: MatchScoreUpdate,
    db: AsyncSession = Depends(get_db)
):
    score = await db.scalar(select(MatchScores).where(MatchScores.score_id == score_id))
    if not score:
        raise HTTPException(status_code=404, detail="Match score not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(score, field, value)

    await db.commit()
    await db.refresh(score)
    return score

#Delete
@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match_score(score_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    score = await db.scalar(select(MatchScores).where(MatchScores.score_id == score_id))
    if not score:
        raise HTTPException(status_code=404, detail="Match score not found")

    await db.delete(score)
    await db.commit()