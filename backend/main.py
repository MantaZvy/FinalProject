import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from sqlalchemy import text
from models import JobDescriptions, JobSeeker, Applications, Documents, CalendarEvents, EmailEvents, MatchScores, NlpLogs

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Pydantic Schemas
# ----------------------
class JobDescriptionsSchema(BaseModel):
    job_id: Optional[uuid.UUID]
    title: Optional[str]
    company: Optional[str]
    description: Optional[str]
    skills_required: Optional[List[str]]
    keywords: Optional[List[str]]
    source: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class JobSeekerSchema(BaseModel):
    user_id: Optional[uuid.UUID]
    profile_summary: Optional[str]
    skills: Optional[List[str]]
    education: Optional[dict]
    experience: Optional[dict]
    certifications: Optional[List[str]]
    keywords: Optional[List[str]]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class NlpLogsSchema(BaseModel):
    run_id: Optional[uuid.UUID]
    model_name: Optional[str]
    bleu_score: Optional[float]
    perplexity: Optional[float]
    accuracy: Optional[float]
    notes: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class ApplicationsSchema(BaseModel):
    application_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    job_title: Optional[str]
    company: Optional[str]
    job_id: Optional[uuid.UUID]
    platform: Optional[str]
    status: Optional[str]
    salary_range: Optional[str]
    notes: Optional[str]
    applied_date: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class DocumentsSchema(BaseModel):
    document_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    doc_type: Optional[str]
    content: Optional[str]
    file_path: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class CalendarEventsSchema(BaseModel):
    event_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    event_title: Optional[str]
    event_date: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    google_event_id: Optional[str]

    class Config:
        orm_mode = True

class EmailEventsSchema(BaseModel):
    email_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    sender: Optional[str]
    subject: Optional[str]
    snippet: Optional[str]
    detected_status: Optional[str]
    received_at: Optional[datetime.datetime]
    processed_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class MatchScoresSchema(BaseModel):
    score_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    job_id: Optional[uuid.UUID]
    similarity_score: Optional[float]
    regression_prediction: Optional[float]
    model_used: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

# ----------------------
# Endpoints
# ----------------------

# Jobs
@app.get("/jobs", response_model=List[JobDescriptionsSchema])
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobDescriptions))
    return result.scalars().all()

@app.post("/jobs", response_model=JobDescriptionsSchema)
async def add_job(job: JobDescriptionsSchema, db: AsyncSession = Depends(get_db)):
    new_job = JobDescriptions(**job.dict(exclude_unset=True))
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

# Job Seekers
@app.get("/job_seekers", response_model=List[JobSeekerSchema])
async def get_job_seekers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobSeeker))
    return result.scalars().all()

@app.post("/job_seekers", response_model=JobSeekerSchema)
async def add_job_seeker(user: JobSeekerSchema, db: AsyncSession = Depends(get_db)):
    new_user = JobSeeker(**user.dict(exclude_unset=True))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Applications
@app.get("/applications", response_model=List[ApplicationsSchema])
async def get_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Applications))
    return result.scalars().all()

@app.post("/applications", response_model=ApplicationsSchema)
async def add_application(application: ApplicationsSchema, db: AsyncSession = Depends(get_db)):
    new_app = Applications(**application.dict(exclude_unset=True))
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app

# Documents
@app.get("/documents", response_model=List[DocumentsSchema])
async def get_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Documents))
    return result.scalars().all()

@app.post("/documents", response_model=DocumentsSchema)
async def add_document(doc: DocumentsSchema, db: AsyncSession = Depends(get_db)):
    new_doc = Documents(**doc.dict(exclude_unset=True))
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

# Calendar Events
@app.get("/calendar_events", response_model=List[CalendarEventsSchema])
async def get_calendar_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CalendarEvents))
    return result.scalars().all()

@app.post("/calendar_events", response_model=CalendarEventsSchema)
async def add_calendar_event(event: CalendarEventsSchema, db: AsyncSession = Depends(get_db)):
    new_event = CalendarEvents(**event.dict(exclude_unset=True))
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

# Email Events
@app.get("/email_events", response_model=List[EmailEventsSchema])
async def get_email_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailEvents))
    return result.scalars().all()

@app.post("/email_events", response_model=EmailEventsSchema)
async def add_email_event(email: EmailEventsSchema, db: AsyncSession = Depends(get_db)):
    new_email = EmailEvents(**email.dict(exclude_unset=True))
    db.add(new_email)
    await db.commit()
    await db.refresh(new_email)
    return new_email

# Match Scores
@app.get("/match_scores", response_model=List[MatchScoresSchema])
async def get_match_scores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MatchScores))
    return result.scalars().all()

@app.post("/match_scores", response_model=MatchScoresSchema)
async def add_match_score(score: MatchScoresSchema, db: AsyncSession = Depends(get_db)):
    new_score = MatchScores(**score.dict(exclude_unset=True))
    db.add(new_score)
    await db.commit()
    await db.refresh(new_score)
    return new_score

# NLP Logs
@app.get("/nlp_logs", response_model=List[NlpLogsSchema])
async def get_nlp_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NlpLogs))
    return result.scalars().all()

@app.post("/nlp_logs", response_model=NlpLogsSchema)
async def add_nlp_log(log: NlpLogsSchema, db: AsyncSession = Depends(get_db)):
    new_log = NlpLogs(**log.dict(exclude_unset=True))
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

# Root
@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/test-db")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "connected", "result": value}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
