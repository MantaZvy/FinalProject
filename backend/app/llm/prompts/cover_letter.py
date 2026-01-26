def build_cover_letter_prompt(
    candidate_name: str,
    job_title: str,
    company_name: str,
    resume_summary: str,
    matched_skills: list[str],
) -> str:
    return f"""
You are a professional career assistant.

Write a tailored cover letter for the following candidate.

Candidate name: {candidate_name}
Role applied for: {job_title}
Company: {company_name}

Candidate profile:
{resume_summary}

Key matched skills:
{", ".join(matched_skills)}

Rules:
- Professional and confident tone
- No emojis
- Do not mention missing skills
- One page and 250 words maximum
"""