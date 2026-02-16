from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

SKILL_ALIASES = {
    "postgres": "postgresql",
    "psql": "postgresql",
    "postgre": "postgresql",
    "fast api": "fastapi",
    "sql alchemy": "sqlalchemy",
    "py": "python",
    "node js": "nodejs",
    "js": "javascript"
}

def clean_text(text: str) -> str:#to lowercase for better matching
    return re.sub(r"[^a-z0-9\s]", "", text.lower()).strip()

def normalise_skill(text: str) -> str:
    cleaned = clean_text(text)
    return SKILL_ALIASES.get(cleaned, cleaned)#apply normalisation alias layer

def build_resume_text(resume: Dict[str, Any]) -> str:
    parts = []
    #extraction of raw text
    parts.extend([normalise_skill(skill) for skill in resume.get("skills", [])])
    parts.extend([clean_text(keyword) for keyword in resume.get("keywords", [])])

    exp = resume.get("experience")
    if isinstance(exp, dict):
        parts.append(clean_text(" ".join([
            exp.get("role", ""),
            exp.get("company", ""),
            exp.get("description", "")
        ])))

    elif isinstance(exp, list):
        for item in exp:
            if isinstance(item, dict):
                parts.append(clean_text(" ".join([
                    item.get("role", ""),
                    item.get("company", ""),
                    item.get("description", "")
                ])))
            else:
                parts.append(clean_text(str(item)))
    return " ".join(parts)
    
def build_job_text(job: Dict[str, Any]) ->str:
    parts = []
    #extraction of job raw required text
    if job.get("title"):
        parts.append(clean_text(job["title"]))
    if job.get("description"):
        parts.append(clean_text(job["description"]))
    parts.extend([
        normalise_skill(skill)
        for skill in job.get("skills_required", [])
    ])
    if job.get("keywords"):
        parts.extend([clean_text(k) for k in job["keywords"]])
    return " ".join(parts)

def tfidf_match(resume: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    resume_text = build_resume_text(resume)
    job_text = build_job_text(job)
    if not resume_text.strip() or not job_text.strip():
        return{
            "model_name": "tfidf",
            "model_version":"v1",
            "similarity_score": 0.0,
        }
        
    vectorizer = TfidfVectorizer(ngram_range=(1, 2),
        stop_words="english")  
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return{
        "model_name": "tfidf",
        "model_version": "v1",
        "similarity_score": float(similarity),
    }