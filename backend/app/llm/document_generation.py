from app.llm.client import LLMClient
from app.llm.prompts.resume import build_resume_prompt
from app.llm.prompts.cover_letter import build_cover_letter_prompt


class DocumentGenerator:
    def __init__(self, provider: str = "ollama"):
        self.llm = LLMClient(provider)

    async def generate_resume(
        self,
        candidate_name: str,
        current_role: str,
        years_experience: int,
        skills: list[str],
        target_role: str,
    ) -> str:
        prompt = build_resume_prompt(
            candidate_name=candidate_name,
            current_role=current_role,
            years_experience=years_experience,
            skills=skills,
            target_role=target_role,
        )
        return await self.llm.generate(prompt)

    async def generate_cover_letter(
        self,
        candidate_name: str,
        target_company: str,
        target_role: str,
        matched_skills: list[str],
    ) -> str:
        prompt = build_cover_letter_prompt(
            candidate_name=candidate_name,
            target_company=target_company,
            target_role=target_role,
            matched_skills=matched_skills,
        )
        return await self.llm.generate(prompt)


_generator = DocumentGenerator(provider="ollama")


async def generate_resume(input_data: dict) -> dict:
    candidate = input_data["candidate"]
    job = input_data["job"]

    experience = candidate.get("experience", [])

    content = await _generator.generate_resume(
    
        candidate_name=candidate.get("candidate_name", "Unknown Candidate"),

        
        current_role=experience[0] if experience else "Software Developer",

        years_experience=max(len(experience) // 3, 1),

        skills=candidate.get("skills", []),
        target_role=job.get("title", "Unknown Role"),
    )

    return {
        "content": content,
        "model": "mistral",
        "prompt_version": "resume_v1",
    }


async def generate_cover_letter(input_data: dict) -> dict:
    candidate = input_data["candidate"]
    job = input_data["job"]
    match = input_data["match"]

    content = await _generator.generate_cover_letter(
        candidate_name=candidate.get("candidate_name", "Unknown Candidate"),
        target_company=job.get("company", "Unknown Company"),
        target_role=job.get("title", "Unknown Role"),
        matched_skills=match.get("matched_skills", []),
    )

    return {
        "content": content,
        "model": "mistral",
        "prompt_version": "cover_letter_v1",
    }