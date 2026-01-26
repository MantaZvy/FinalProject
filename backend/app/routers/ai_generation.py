from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import Applications, JobDescriptions, Documents, MatchScores
from app.nlp.generation.input_builder import build_generation_input
from app.llm.document_generation import generate_resume, generate_cover_letter
import uuid

router = APIRouter(prefix="/ai/generate", tags=["AI Generation"])

@router.post(
    "/resume/{application_id}",
    status_code=status.HTTP_200_OK,
)
async def generate_resume_for_application(
    application_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

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

    match_score = await db.scalar(
        select(MatchScores)
        .where(MatchScores.application_id == application.application_id)
        .order_by(MatchScores.created_at.desc())
    )
    if not match_score:
        raise HTTPException(status_code=404, detail="Match score not found")

    generation_input = build_generation_input(
        application=application,
        resume=resume,
        job=job,
        match_score=match_score,
    )

    result = await generate_resume(generation_input)

    return {
        "document_type": "resume",
        "content": result["content"],
        "model": result["model"],
        "prompt_version": result["prompt_version"],
    }

@router.post(
    "/cover-letter/{application_id}",
    status_code=status.HTTP_200_OK,
)
async def generate_cover_letter_for_application(
    application_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    application = await db.scalar(
        select(Applications).where(Applications.application_id == application_id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

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

    match_score = await db.scalar(
        select(MatchScores)
        .where(MatchScores.application_id == application.application_id)
        .order_by(MatchScores.created_at.desc())
    )
    if not match_score:
        raise HTTPException(status_code=404, detail="Match score not found")

    generation_input = build_generation_input(
        application=application,
        resume=resume,
        job=job,
        match_score=match_score,
    )

    result = await generate_cover_letter(generation_input)

    return {
        "document_type": "cover_letter",
        "content": result["content"],
        "model": result["model"],
        "prompt_version": result["prompt_version"],
    }
