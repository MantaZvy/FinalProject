def build_cover_letter_prompt(
    candidate_name: str,
    target_company: str,
    target_role: str,
    matched_skills: list[str],
    resume_summary: str | None = None,
) -> str:
    profile_section = resume_summary or "Generate a concise professional candidate summary based on skills and experience."

    return f"""
You are a professional career assistant.

Write a tailored cover letter for the following candidate.

Candidate name: {candidate_name}
Role applied for: {target_role}
Company: {target_company}

Candidate profile:
{profile_section}

Key matched skills:
{", ".join(matched_skills)}

Rules:
- Professional and confident tone
- No emojis
- Do not mention missing skills
- One page and 250 words maximum
- Formal tone
"""