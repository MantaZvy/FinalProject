from typing import Dict, List
import re
import pdfplumber
from fastapi import HTTPException, status
from io import BytesIO


COMMON_SKILLS = [
    "python", "sql", "fastapi", "postgresql",
    "nlp", "machine learning", "docker",
    "aws", "react", "javascript"
]
#text extraction from format logic (ONLY TEXT AND PDF SUPPORTED)
def extract_resume_text(file_bytes: bytes, content_type: str) -> str:
    if content_type == "text/plain":
        return file_bytes.decode("utf-8")

    if content_type == "application/pdf":
        text_chunks = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text_chunks.append(page.extract_text() or "")
        return "\n".join(text_chunks)

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Unsupported file type"
    )

def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    return sorted({skill for skill in COMMON_SKILLS if skill in text_lower})


def extract_profile_summary(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return " ".join(lines[:3])[:500]


def extract_section(text: str, section_name: str) -> str | None:
    pattern = rf"{section_name}[:\n](.*?)(\n[A-Z][a-z]+:|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def parse_resume(text: str) -> Dict:
    return {
        "skills": extract_skills(text),
        "keywords": extract_skills(text),
        "profile_summary": extract_profile_summary(text),
        "education": extract_section(text, "education"),
        "experience": extract_section(text, "experience"),
    }