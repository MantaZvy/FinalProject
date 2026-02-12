from typing import List, Optional

from app.llm.client import LLMClient
from app.llm.prompts.resume import build_resume_prompt
from app.llm.prompts.cover_letter import build_cover_letter_prompt
from app.schemas.experience import ExperienceRoleDict 


def normalize_experience(raw_experience: List[str]) -> List[ExperienceRoleDict]:
    roles: List[ExperienceRoleDict] = []
    current: Optional[ExperienceRoleDict] = None

    for line in raw_experience:
        line = line.strip()
        if not line:
            continue

        if " - " in line:
            if current is not None:
                roles.append(current)

            current = {
                "company_and_dates": line,
                "title": None,
                "bullets": [],
            }
            continue

        if current is None:
            continue

        if current["title"] is None and len(line.split()) <= 5:
            current["title"] = line
        else:
            current["bullets"].append(line)

    if current is not None:
        roles.append(current)

    return roles



class DocumentGenerator:
    def __init__(self, provider: str = "ollama"):
        self.llm = LLMClient(provider)

    async def generate_resume(
    self,
    candidate_name: str,
    structured_experience: List[ExperienceRoleDict],
    skills: List[str],
    target_role: str,
) -> str:

        prompt = build_resume_prompt(
            candidate_name=candidate_name,
            structured_experience=structured_experience,
            skills=skills,
            target_role=target_role,
        )
        return await self.llm.generate(prompt)

    async def generate_cover_letter(
    self,
    candidate_name: str,
    structured_experience: List[ExperienceRoleDict],
    skills: List[str],
    target_company: str,
    target_role: str,
    matched_skills: List[str],
    job_description: str,
    job_required_skills: List[str],
) -> str:
        prompt = build_cover_letter_prompt(
            candidate_name=candidate_name,
            structured_experience=structured_experience,
            skills=skills,
            target_company=target_company,
            target_role=target_role,
            matched_skills=matched_skills,
            job_description=job_description,
            job_required_skills=job_required_skills,
        )
        return await self.llm.generate(prompt)


_generator = DocumentGenerator(provider="ollama")


async def generate_resume(input_data: dict) -> dict:
    candidate = input_data["candidate"]
    job = input_data["job"]

    raw_experience = candidate.get("experience", [])
    structured_experience = normalize_experience(raw_experience)

    content = await _generator.generate_resume(
        candidate_name=candidate.get("name", "Unknown Candidate"),
        structured_experience=structured_experience,
        skills=candidate.get("skills", []),
        target_role=job.get("title", "Unknown Role"),
    )

    return {
        "content": content,
        "model": "mistral",
        "prompt_version": "resume_v2",
    }


async def generate_cover_letter(input_data: dict) -> dict:
    candidate = input_data["candidate"]
    job = input_data["job"]
    match = input_data["match"]

    raw_experience = candidate.get("experience", [])
    structured_experience = normalize_experience(raw_experience)

    content = await _generator.generate_cover_letter(
    candidate_name=candidate.get("name", "Unknown Candidate"),
    structured_experience=structured_experience,
    skills=candidate.get("skills", []),
    target_company=job.get("company_name") or job.get("company") or "Unknown Company",
    target_role=job.get("job_title") or job.get("title") or "Unknown Role",
    matched_skills=match.get("matched_skills", []),
    job_description=job.get("description", ""),
    job_required_skills=job.get("skills_required", []),

)

    return {
        "content": content,
        "model": "mistral",
        "prompt_version": "cover_letter_v1",
    }
