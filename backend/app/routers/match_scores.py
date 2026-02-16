from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.match_score import MatchScoreCreate, MatchScoreUpdate, MatchScoreOut
from app.nlp.match_scorer import keyword_overlap_matcher, weighted_skill_matcher
from app.nlp.model_selector import select_best_model
from app.models import MatchScores, Applications, JobDescriptions, JobSeeker, Documents
from app.nlp.recommendations import generate_recommendations
from app.db import get_db
from app.nlp.tfidf_matcher import tfidf_match
import uuid
import re

router = APIRouter(prefix="/match_scores", tags=["Match Scores"])

# Match Score endpoints
#create
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
    
#ensures resume data is always structured for NLP models
def normalize_resume(content):
    if isinstance(content, dict):
        return {
            "skills": content.get("skills", []),
            "keywords": content.get("keywords", []),
        }

    if isinstance(content, str):
        tokens = re.findall(r"\b[a-zA-Z]+\b", content.lower())
        return {
            "skills": tokens,
            "keywords": tokens,
        }

    return {"skills": [], "keywords": []}

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
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    user = await db.scalar(
    select(JobSeeker).where(JobSeeker.user_id == application.user_id)
)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    job = await db.scalar(
        select(JobDescriptions).where(JobDescriptions.job_id == application.job_id)
    )
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume = await db.scalar(
        select(Documents)
        .where(
            Documents.user_id == application.user_id,
            Documents.doc_type == "resume",
        )
        .order_by(Documents.created_at.desc())
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    
    job_data = {
        "title": job.title or "",
        "description": job.description or "",
        "skills_required": job.skills_required or [],
        "keywords": job.keywords or [],
    }
    resume_data = {
    "skills": user.skills or [],
    "keywords": user.keywords or [],
    "experience": user.experience,
}
    results = [
        keyword_overlap_matcher(resume_data, job_data),
        weighted_skill_matcher(resume_data, job_data),
        tfidf_match(resume_data, job_data),
    ]
    print("MODEL RESULTS:", results)

    best = select_best_model(results)

    score = MatchScores(
        user_id=application.user_id,
        application_id=application.application_id,
        job_id=job.job_id,
        similarity_score=best["similarity_score"],
        model_used=f'{best["model_name"]}:{best["model_version"]}',
        matched_skills=best.get("matched_skills", []),
        missing_skills=best.get("missing_skills", []),
        explanation=(
            f"Matched skills: {', '.join(best.get('matched_skills', []))}. "
            f"Missing skills: {', '.join(best.get('missing_skills', []))}."
            if best.get("matched_skills") or best.get("missing_skills")
            else "No significant skill overlap detected."
        ),
    )
 

    db.add(score)
    await db.commit()
    await db.refresh(score)

    recommendations = generate_recommendations(score.missing_skills or [])

    return {#dynamic generation with recs
        **score.__dict__,
        "recommendations": recommendations,
    }