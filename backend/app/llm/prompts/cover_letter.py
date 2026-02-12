def build_cover_letter_prompt(
    candidate_name: str,
    structured_experience: list[dict],
    skills: list[str],
    target_company: str,
    target_role: str,
    matched_skills: list[str],
    job_description: str,
    job_required_skills: list[str],
) -> str:

    experience_block = []

    for role in structured_experience:
        experience_block.append(
            f"""
Company & Dates: {role.get("company_and_dates", "N/A")}
Title: {role.get("title", "N/A")}
Responsibilities:
- """ + "\n- ".join(role.get("bullets", []))
        )

    experience_text = "\n".join(experience_block)

    return f"""
You are a professional cover letter writer.

Write a tailored cover letter using ONLY the information provided.

You MUST NOT:
- Invent years of experience
- Invent previous companies
- Invent metrics or achievements
- Claim seniority
- Add technologies not listed

Candidate Name:
{candidate_name}

Role Applied For:
{target_role}

Company:
{target_company}

Candidate Skills:
{", ".join(skills)}

Matched Skills:
{", ".join(matched_skills)}

Job Required Skills:
{", ".join(job_required_skills)}

Job Description:
{job_description}

Work Experience:
{experience_text}

Instructions:
- Align the candidate to the role realistically
- Emphasize transferable strengths where direct match is limited
- Use confident but grounded tone
- Avoid generic phrases
- Do not fabricate experience
- Do not add placeholders
- No emojis
- 200 words max
"""