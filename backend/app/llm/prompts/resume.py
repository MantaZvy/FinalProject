
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

    return f"""You are an expert technical resume strategist.

Your task is to transform the candidate's raw experience into a compelling, ATS-optimized resume tailored to the target role.

You may enhance bullets with realistic impact framing and contextual detail, but you must not fabricate:
- Specific numbers or metrics
- Tools not listed
- Additional roles
- Years of experience

If metrics are not provided, describe outcomes in terms of impact, efficiency, collaboration, scale, or problem-solving without inventing numbers.

Position the candidate as an aspiring {target_role} with strong technical foundations and transferable experience.

Candidate Name:
{candidate_name}

Target Role:
{target_role}

Skills (use exactly as written, but you may group them strategically):
{", ".join(skills)}

Work Experience:
{experience_text}

Output Requirements:
- Strong professional summary aligned with the target role
- Impact-focused bullet points (not duty descriptions)
- Clean ATS-friendly formatting
- No placeholders
- No emojis
- No generic filler language
- No mention of these instructions
"""