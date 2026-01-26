def build_resume_prompt(
    candidate_name: str,
    current_role: str,
    years_experience: int,
    skills: list[str],
    target_role: str,
) -> str:
    return f"""
You are a professional resume writer, helping applicants to write a professional, ATS-friendly resume.

Generate a tailored resume for the candidate below.

Candidate name: {candidate_name}
Current role: {current_role}
Years of experience: {years_experience}
Target role: {target_role}

Core skills:
{", ".join(skills)}

Rules:
- Use concise bullet points
- No emojis
- ATS-friendly formatting
- One page maximum
"""