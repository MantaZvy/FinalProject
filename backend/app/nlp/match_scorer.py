from typing import Dict, List, Set, Any
from app.nlp.types import MatchResult

#normalise a list of strings by converting to lowercase and stripping whitespace
def normalize(values: List[str] | None) -> Set[str]:
    if not values:
        return set()
    return {v.lower().strip() for v in values}

def compute_match_score(
    resume: Dict[str, Any],
    job: Dict[str, Any]
) -> Dict[str, Any]:
    
    resume_skills = normalize(resume.get("skills"))
    job_skills = normalize(job.get("skills"))

    resume_keywords = normalize(resume.get("keywords"))
    job_keywords = normalize(job.get("keywords"))

    matched_skills = sorted(resume_skills & job_skills)
    matched_keywords = sorted(resume_keywords & job_keywords)

    #weights
    SKILL_WEIGHT = 0.7
    KEYWORD_WEIGHT = 0.3

    skill_score = (
        len(matched_skills) / max(len(job_skills), 1)
    ) * 100

    keyword_score = (
        len(matched_keywords) / max(len(job_keywords), 1)
    ) * 100

    total_score = round(
        (skill_score * SKILL_WEIGHT) +
        (keyword_score * KEYWORD_WEIGHT),
        2
    )

    explanation = (
        f"Matched skills: {', '.join(matched_skills)}. "
        f"Matched keywords: {', '.join(matched_keywords)}."
        if matched_skills or matched_keywords
        else "No significant matches found."
    )

    return {
        "similarity_score": total_score,
        "model_used": "skill_keyword_overlap_v1",
        "matched_skills": matched_skills,
        "matched_keywords": matched_keywords,
        "explanation": explanation
    }
    
def keyword_overlap_matcher(resume: dict, job: dict) -> MatchResult:
    resume_skills = set(resume.get("skills", []))
    job_skills = set(job.get("skills", []))

    resume_keywords = set(resume.get("keywords", []))
    job_keywords = set(job.get("keywords", []))

    matched_skills = list(resume_skills & job_skills)
    matched_keywords = list(resume_keywords & job_keywords)

    total_possible = len(job_skills | job_keywords)
    total_matched = len(matched_skills) + len(matched_keywords)

    score = total_matched / total_possible if total_possible else 0.0

    return {
        "similarity_score": round(score, 4),
        "matched_skills": matched_skills,
        "matched_keywords": matched_keywords,
        "model_name": "keyword_overlap",
        "model_version": "v1",
    }