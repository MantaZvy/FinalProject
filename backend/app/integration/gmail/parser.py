import re

STATUS_RULES = {
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
def detect_application_status(text: str) -> str:
    text = text.lower()
    for status, keywords in STATUS_RULES.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                return status
    return "unknown"