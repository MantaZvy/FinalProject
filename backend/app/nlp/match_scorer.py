from typing import Dict, Any
from app.nlp.types import MatchResult
from app.nlp.normalise import normalize_skills
from app.nlp.tfidf_matcher import tfidf_match


def extract_resume_skills(resume: Dict[str, Any]) -> set[str]:
    skills = set()

    skills |= normalize_skills(resume.get("profile_skills", []))

    skills |= normalize_skills(resume.get("skills", []))

    skills |= normalize_skills(resume.get("keywords", []))

    return skills

def keyword_overlap_matcher(resume: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:#catches literal matching missed by TF-IDF
    resume_skills = extract_resume_skills(resume)
    job_skills = normalize_skills(job.get("skills", []))

    if not job_skills:
        return {
            "model_name": "keyword_overlap",
            "model_version": "v2",
            "similarity_score": 0.0,
            "matched_skills": [],
            "matched_keywords": [],
        }

    matched = resume_skills & job_skills
    score = len(matched) / len(job_skills)

    return {
        "model_name": "keyword_overlap",
        "model_version": "v2",
        "similarity_score": round(score, 3),
        "matched_skills": sorted(matched),
        "matched_keywords": [],
    }

def weighted_skill_matcher(resume: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:#enforces job requirements (hard match signal)
    
    resume_skills = extract_resume_skills(resume)
    job_skills = normalize_skills(job.get("skills", []))

    if not job_skills:
        return {
            "model_name": "weighted_skill",
            "model_version": "v2",
            "similarity_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    base_score = len(matched) / len(job_skills)
    weighted_score = min(base_score * 1.25, 1.0)

    return {
        "model_name": "weighted_skill",
        "model_version": "v2",
        "similarity_score": round(weighted_score, 3),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
    }
    
def final_match(resume: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:

    tfidf_result = tfidf_match(resume, job)#detects semantic logic
    skill_result = weighted_skill_matcher(resume, job)
    keyword_result = keyword_overlap_matcher(resume, job)

    tfidf_score = tfidf_result["similarity_score"]
    skill_score = skill_result["similarity_score"]
    keyword_score = keyword_result["similarity_score"]

    #hybrid scoring logic
    final_score = (
        0.6 * tfidf_score +#meaning
        0.3 * skill_score +#requirements
        0.1 * keyword_score#fallback signal
    )

    return {
        "model_name": "hybrid_match",
        "model_version": "v1",
        "similarity_score": round(final_score, 3),

        "tfidf_score": tfidf_score,
        "skill_score": skill_score,
        "keyword_score": keyword_score,

        "matched_skills": skill_result.get("matched_skills", []),
        "missing_skills": skill_result.get("missing_skills", []),
    }