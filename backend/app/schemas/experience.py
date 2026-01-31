from typing import TypedDict, List, Optional


class ExperienceRoleDict(TypedDict):
    company_and_dates: str
    title: Optional[str]
    bullets: List[str]

