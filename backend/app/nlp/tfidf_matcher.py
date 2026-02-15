from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_resume_text(resume: Dict[str, Any]) -> str:
    parts = []
    #extraction of resume raw text
    skills = resume.get("skills", [])
    parts.extend(skills)
    keywords = resume.get("keywords", [])
    parts.extend(keywords)
    experience = resume.get("experience", [])
    parts.extend(experience)
    
    return " ".join(parts)
    
def build_job_text(job: Dict[str, Any]) ->str:
    parts = []
    #extraction of job raw required text
    parts.extend(job.get("skills",[]))
    parts.extend(job.get("keywords", []))
    desc = job.get("description", "")
    if isinstance(desc, str):
        parts.append(desc)
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
        
    vectorizer = TfidfVectorizer(stop_words="english")
    
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return{
        "model_name": "tfidf",
        "model_version": "v1",
        "similarity_score": similarity,
    }