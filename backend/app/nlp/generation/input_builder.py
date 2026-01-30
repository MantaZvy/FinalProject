def build_generation_input(
    application,
    resume,
    job,
    match_score,
) -> dict:

    resume_data = resume.content
    if isinstance(resume_data, str):
        import json
        resume_data = json.loads(resume_data)

    candidate = {
        "name": resume_data.get("candidate_name"),
        "skills": resume_data.get("skills", []),
        "experience": resume_data.get("experience", []),
        "summary": resume_data.get("resume_summary"),
    }

    job_data = {
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "skills_required": job.skills_required or [],
    }

    match = {
        "matched_skills": match_score.matched_skills or [],
        "missing_skills": match_score.missing_skills or [],
        "similarity_score": match_score.similarity_score,
    }

    return {
        "candidate": candidate,
        "job": job_data,
        "match": match,
        "application_id": application.application_id,
        "user_id": application.user_id,
    }