from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.match_score import MatchScoreCreate, MatchScoreUpdate, MatchScoreOut, MatchScoreCompute
from app.nlp.match_scorer import compute_match_score
from app.models import MatchScores, Applications, JobDescriptions, JobSeeker, Documents
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
    
#Computed Match Score NLP/ML Endpoint and return MatchScoreOut, create POST
@router.post(
    "/compute/{application_id}",
    response_model=MatchScoreOut,
    status_code=status.HTTP_201_CREATED,
)
async def compute_match_score_for_application(
    application_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    application = await db.scalar(#fetch application
        select(Applications).where(
            Applications.application_id == application_id
        )
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = await db.scalar(#fetch job description
        select(JobDescriptions).where(
            JobDescriptions.job_id == application.job_id
        )
    )
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume = await db.scalar(#latest resume document 
        select(Documents)
        .where(
            Documents.user_id == application.user_id,
            Documents.doc_type == "resume",
        )
        .order_by(Documents.created_at.desc())
    )
    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found for user",
        )

    resume_data = resume.content if isinstance(resume.content, dict) else {}#build nlp input
    job_data = {
        "skills": job.skills or [],
        "keywords": job.keywords or [],
    }

    result = compute_match_score(#compute match score
        resume=resume_data,
        job=job_data,
    )

    score = MatchScores(
        user_id=application.user_id,
        application_id=application.application_id,
        job_id=job.job_id,
        similarity_score=result["score"],
        model_used="keyword_skill_match_v1",
    )

    db.add(score)
    await db.commit()
    await db.refresh(score)

    return score
#Compute match score with parsed job and resume data
@router.post(
    "/compute",
    response_model=MatchScoreOut,
    status_code=status.HTTP_201_CREATED
)
async def compute_and_store_match_score(
    payload: MatchScoreCompute,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(JobSeeker, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    application = await db.get(Applications, payload.application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = await db.get(JobDescriptions, payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume_data = {
        "skills": user.skills or [],
        "keywords": user.keywords or [],
    }

    job_data = {
        "skills": job.skills_required or [],
        "keywords": job.keywords or [],
    }

    result = compute_match_score(resume_data, job_data)

    match_score = MatchScores(
        user_id=payload.user_id,
        application_id=payload.application_id,
        job_id=payload.job_id,
        similarity_score=result["score"],
        model_used="skill_keyword_overlap_v1",
    )

    db.add(match_score)
    await db.commit()
    await db.refresh(match_score)

    return match_score
