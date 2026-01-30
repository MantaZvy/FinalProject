from typing import TypedDict, Optional, List

class ExperienceRole(TypedDict):
    company_and_dates: str
    title: Optional[str]
    bullets: List[str]
