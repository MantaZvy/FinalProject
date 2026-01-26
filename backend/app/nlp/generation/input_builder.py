from typing import Dict, Any
from app.models import Applications, JobDescriptions, Documents, MatchScores


def build_generation_input(
    application: Applications,
    resume: Documents,
    job: JobDescriptions,
    match_score: MatchScores,
) -> Dict[str, Any]:

    resume_content = resume.content if isinstance(resume.content, dict) else {}

    return {
        "candidate": {
            "skills": resume_content.get("skills", []),
            "experience": resume_content.get("experience", []),
            "education": resume_content.get("education", []),
        },
        "job": {
            "title": job.title,
            "company": job.company_name,
            "requirements": job.skills_required or [],
            "keywords": job.keywords or [],
        },
        "match": {
            "similarity_score": match_score.similarity_score,
            "matched_skills": getattr(match_score, "matched_skills", []),
            "missing_skills": getattr(match_score, "missing_skills", []),
        },
        "application_metadata": {
         "application_id": str(application.application_id),
         "submission_date": str(application.created_at),
        }
    }