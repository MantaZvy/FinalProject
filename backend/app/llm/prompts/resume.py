def build_resume_prompt(
    candidate_name: str,
    current_role: str,
    years_experience: int,
    skills: list[str],
    target_role: str,
    resume_summary: str | None = None,
) -> str:
    profile_section = resume_summary or "Generate a concise professional candidate summary highlighting key achievements and experience."

    return f"""
You are a professional career assistant.

Write a tailored resume for the following candidate.

Candidate name: {candidate_name}
Current role: {current_role}
Years of experience: {years_experience}
Target role: {target_role}

Candidate profile:
{profile_section}

Key skills:
{", ".join(skills)}

Rules:
- Professional and confident tone
- No emojis
- Focus on accomplishments and measurable results
- Keep it concise and structured
- Maximum 2 pages
"""