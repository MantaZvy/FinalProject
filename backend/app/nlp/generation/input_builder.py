import re, json

def parse_experience_to_structured(experience_raw) -> list[dict]:
    if not experience_raw:
        return []
    if isinstance(experience_raw, list):
        structured = []
        for item in experience_raw:
            if isinstance(item,dict):
                structured.append({
                    "company_and_dates": f"{item.get('company', '')} {item.get('years', '')}".strip(),
                    "title": item.get("role", ""),
                    "bullets": [item.get("description", "")] if item.get("description") else []
                })
            else:
                structured.append({
                    "company_and_dates": str(item),
                    "title": "",
                    "bullets": []
                })
            return structured
    if isinstance(experience_raw, str):
        roles = []
        lines = [l.strip() for l in experience_raw.split("\n") if l.strip()]
        current_role: dict = {}

        for line in lines:
            is_header = bool(re.search(
                r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Present|\d{4})",
                line, re.IGNORECASE
            ))

            if is_header and len(line) < 80:
                if current_role:
                    roles.append(current_role)
                current_role = {
                    "company_and_dates": line,
                    "title": "",
                    "bullets": []
                }
            elif current_role:
                title = current_role.get("title", "")
                if not title:
                    current_role["title"] = line
                else:
                    if len(line) > 10:
                        bullets = current_role.get("bullets", [])
                        bullets.append(line)
                        current_role["bullets"] = bullets

        if current_role:
            roles.append(current_role)

        return roles if roles else [{
            "company_and_dates": "",
            "title": "Various Roles",
            "bullets": [experience_raw[:500]]
        }]

def build_generation_input(
    application,
    resume,
    job,
    match_score,
) -> dict:

    resume_data = resume.content
    if isinstance(resume_data, str):
        try:
            resume_data = json.loads(resume_data)
        except Exception:
            resume_data = {}

    raw_experience = resume_data.get("experience", [])
    structured_experience = parse_experience_to_structured(raw_experience)

    candidate = {
        "name": resume_data.get("candidate_name", "Candidate"),
        "skills": resume_data.get("skills", []),
        "experience": resume_data.get("experience", ""),
        "structured_experience": structured_experience,
        "summary": resume_data.get("resume_summary", ""),
    }

    job_data = {
        "title": application.job_title or job.title,
        "company": application.company or job.company,
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