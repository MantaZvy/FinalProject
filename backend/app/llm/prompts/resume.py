
def build_resume_prompt(
    candidate_name: str,
    structured_experience: list[dict],
    skills: list[str],
    target_role: str,
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

    return f"""You are a professional resume editor.

Your task is to REWRITE the candidate's resume using ONLY the information provided.
DO NOT invent roles, years of experience, achievements, metrics, or responsibilities.
DO NOT infer seniority.
DO NOT add skills not listed.

Candidate Name:
{candidate_name}

Target Role:
{target_role}

Skills (use exactly as written):
{", ".join(skills)}

Work Experience (verbatim source data):
{experience_text}

Instructions:
- Rewrite into a clean, professional resume format
- Preserve factual accuracy exactly
- You may rephrase wording for clarity, but not add new facts
- If information is missing, leave it out
- No placeholders such as [Insert], [Prior Experience], or fabricated metrics
- No emojis
"""