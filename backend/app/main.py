from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db import get_db
from app.integration.gmail.gmail_sync import start_scheduler
from app.routers import jobs, applications, documents, match_scores, nlp_logs, calendar_events, email_events, job_seekers, nlp, ai_generation


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

#router registration
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(documents.router)
app.include_router(match_scores.router)
app.include_router(nlp_logs.router)
app.include_router(calendar_events.router)
app.include_router(email_events.router)
app.include_router(job_seekers.router)
app.include_router(nlp.router)
app.include_router(ai_generation.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("Gmail sync scheduler started — polling every 5 minutes") 

# Root endpoints
@app.get("/")
def read_root():
    return {"message": "Backend is running!"}




