from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db import get_db
from app.routers import jobs, applications, documents, match_scores, nlp_logs, calendar_events, email_events, job_seekers, nlp_processing

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
app.include_router(nlp_processing.router)

# Root endpoints
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


