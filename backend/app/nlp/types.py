from typing import List, TypedDict

class MatchResult(TypedDict):
    model_name: str
    model_version: str
    similarity_score: float
    matched_skills: List[str]
    missing_skills: List[str]

