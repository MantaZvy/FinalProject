from typing import Dict, Any
from app.nlp.types import MatchResult
from app.nlp.normalise import normalize_skills
    
def keyword_overlap_matcher(resume: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:
    resume_skills = normalize_skills(resume.get("skills", []))
    job_skills = normalize_skills(job.get("skills", []))

    if not job_skills:
        return {
            "model_name": "keyword_overlap",
            "model_version": "v1",
            "similarity_score": 0.0,
            "matched_skills": [],
            "matched_keywords": [],
        }

    matched = resume_skills & job_skills
    score = len(matched) / len(job_skills)

    return {
        "model_name": "keyword_overlap",
        "model_version": "v1",
        "similarity_score": round(score, 3),
        "matched_skills": sorted(matched),
        "matched_keywords": [],
    }


def weighted_skill_matcher(resume: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:
    resume_skills = normalize_skills(resume.get("skills", []))
    job_skills = normalize_skills(job.get("skills", []))

    if not job_skills:
        return {
            "model_name": "weighted_skill",
            "model_version": "v1",
            "similarity_score": 0.0,
            "matched_skills": [],
            "matched_keywords": [],
        }

    matched = resume_skills & job_skills
    base_score = len(matched) / len(job_skills)

    weighted_score = min(base_score * 1.25, 1.0)

    return {
        "model_name": "weighted_skill",
        "model_version": "v1",
        "similarity_score": round(weighted_score, 3),
        "matched_skills": sorted(matched),
        "matched_keywords": [],
    }
    