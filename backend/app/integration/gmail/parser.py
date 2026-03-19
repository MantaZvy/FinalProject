import re
from typing import Dict, Optional 
from datetime import datetime, timezone
from dateutil import parser as date_parser

STATUS_RULES: Dict[str, list[str]] = {
    "rejected": [
        "unfortunately",
        "we regret to inform you",
        "not moving forward",
        "unsuccessful",
        "won't be progressing",
        "not selected"
    ],
    "interview": [
        "interview",
        "schedule a call",
        "next stage",
        "further discussion",
        "we'd like to invite you",
        "availability",
        "pleased to invite you"
    ],
    "offer": [
        "offer",
        "congratulations",
        "we are pleased to offer you",
        "employment offer",
        "job offer",
        "we would like to extend an offer"
        ],
    "applied": [
        "application received",
        "thank you for applying",
        "application submitted",
    ]
}
def detect_application_status(subject: str, snippet: str) -> str:
    content = f" {subject} {snippet}".lower()

    for status, keywords in STATUS_RULES.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", content):
                return status

    return "unknown"

INTERVIEW_DATE_PATTERNS = [
    r"\b(?:on\s)?(\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{2,4}\s(?:at\s)?\d{1,2}:\d{2}\s?(?:AM|PM)?)",
    r"\b(?:on\s)?(\d{1,2}/\d{1,2}/\d{2,4}\s(?:at\s)?\d{1,2}:\d{2}\s?(?:AM|PM)?)",
    r"\b(?:on\s)?([A-Za-z]+\s\d{1,2},?\s\d{4}\s(?:at\s)?\d{1,2}:\d{2}\s?(?:AM|PM)?)",
]


def extract_interview_datetime(content: str) -> Optional[datetime]:
    for pattern in INTERVIEW_DATE_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            try:
                parsed = date_parser.parse(match.group(1))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)#timezone aware ISO format
                return parsed
            except Exception:
                pass

    return None

MEETING_LINK_PATTERNS = [
    r"https://meet\.google\.com/[a-zA-Z0-9\-]+",
    r"https://zoom\.us/j/\d+",
    r"https://[a-zA-Z0-9\-]*\.zoom\.us/j/\d+",
    r"https://teams\.microsoft\.com/l/meetup-join/[^\s]+"
]


def extract_meeting_link(content: str) -> str | None: #detects meeting links in email_content
    for pattern in MEETING_LINK_PATTERNS:
        match = re.search(pattern, content)
        if match:
            return match.group(0)

    return None