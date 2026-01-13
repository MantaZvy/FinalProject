from typing import TypedDict, List

class MatchResult(TypedDict):
    similarity_score: float
    matched_skills: List[str]
    matched_keywords: List[str]
    model_name: str
    model_version: str
