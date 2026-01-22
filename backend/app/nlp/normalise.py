import re
from typing import Iterable, Set

STOPWORDS = {
    "and", "or", "with", "to", "of", "in", "for", "on", "as",
    "a", "the", "is", "are", "was", "were", "by", "at"
}

SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "reactjs": "react",
    "nodejs": "node",
    "postgres": "postgresql",
    "fast-api": "fastapi",
}

def normalize_token(token: str) -> str | None:
    token = token.lower().strip()
    token = re.sub(r"[^a-z0-9+#]", "", token)

    if not token or token in STOPWORDS:
        return None

    return SKILL_ALIASES.get(token, token)

def normalize_skills(raw: Iterable[str]) -> Set[str]:
    normalized = set()

    for item in raw:
        token = normalize_token(item)
        if token:
            normalized.add(token)

    return normalized
