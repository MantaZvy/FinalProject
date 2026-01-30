import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.models import Documents
import re
import json

DATABASE_URL = "postgresql+asyncpg://postgres:mypassword@localhost:5432/ai_job_assistant"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def migrate_resumes():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Documents).where(Documents.doc_type == "resume"))
        resumes = result.scalars().all()
        count = 0

        for resume in resumes:
            lines = resume.content.splitlines() if isinstance(resume.content, str) else []

            candidate_name = lines[0].strip() if lines else "Unknown Candidate"

         
            profile_summary = ""
            summary_match = re.search(r"PROFILE SUMMARY\s*(.+?)\s*(?:SKILLS|$)", resume.content, re.DOTALL | re.IGNORECASE)
            if summary_match:
                profile_summary = summary_match.group(1).strip()

         
            skills = []
            skills_match = re.search(r"SKILLS\s*(.+?)\s*(?:PROFESSIONAL EXPERIENCE|$)", resume.content, re.DOTALL | re.IGNORECASE)
            if skills_match:
                skills_lines = skills_match.group(1).splitlines()
                skills = [s.strip() for s in skills_lines if s.strip()]

          
            experience = []
            exp_match = re.search(r"PROFESSIONAL EXPERIENCE\s*(.+?)(?:$)", resume.content, re.DOTALL | re.IGNORECASE)
            if exp_match:
                exp_lines = exp_match.group(1).splitlines()
                experience = [e.strip() for e in exp_lines if e.strip()]

            # store json
            structured_content = {
                "candidate_name": candidate_name,
                "resume_summary": profile_summary,
                "skills": skills,
                "experience": experience,
                "education": [],  # add extraction later if needed
                "raw_text": resume.content,
            }

            resume.content = json.dumps(structured_content)
            count += 1

        await session.commit()
        print(f"Migrated {count} resumes to structured JSON.")

if __name__ == "__main__":
    asyncio.run(migrate_resumes())