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
    for skill in resume.get("skills", []):# added skill weighting by repeating 3x for skill importance
        norm = normalise_skill(skill)
        parts.extend([norm] * 3)
        
    parts.extend([clean_text(keyword) for keyword in resume.get("keywords", [])])

    exp = resume.get("experience")
    if isinstance(exp, dict):
        exp_text = clean_text(" ".join([
            exp.get("role", ""),
            exp.get("company", ""),
            exp.get("description", "")
        ]))
        parts.extend([exp_text] * 2) #boosting experience for importance

    elif isinstance(exp, list):
        for item in exp:
            if isinstance(item, dict):
                exp_text = clean_text(" ".join([        
                    item.get("role", ""),
                    item.get("company", ""),
                    item.get("description", "")
                ]))
                parts.extend([exp_text] * 2)
            else:
                parts.extend([clean_text(str(item))]*2)
                
    return " ".join(parts)
    
def build_job_text(job: Dict[str, Any]) ->str:
    parts = []
    #extraction of job raw required text
    if job.get("title"):
        title = clean_text(job["title"])
        parts.extend([title] * 2)  #boosting job title for importance
        
    if job.get("description"):
        parts.append(clean_text(job["description"]))
        
    for skill in job.get("skills_required", []):
        norm = normalise_skill(skill)
        parts.extend([norm] * 3)#same weighting goes for job required skills
        
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
        
    vectorizer = TfidfVectorizer(ngram_range=(1, 2),stop_words="english", min_df=1, sublinear_tf=True) #using unigrams and bigrams, removing stop words, and applying sublinear tf scaling to better capture important terms and smooth repetition
    
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return{
        "model_name": "tfidf",
        "model_version": "v1",
        "similarity_score": float(similarity),
    }