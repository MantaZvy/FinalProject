from typing import List, Dict

SKILL_RECOMMENDATIONS: Dict[str, Dict[str, str]] = {
    "docker": {
        "recommendation": "Learn Docker to containerize and deploy applications consistently.",
        "category": "DevOps",
    },
    "aws": {
        "recommendation": "Gain experience with AWS services such as EC2, S3, and IAM.",
        "category": "Cloud",
    },
    "react": {
        "recommendation": "Strengthen your React skills for building dynamic user interfaces.",
        "category": "Frontend",
    },
    "typescript": {
        "recommendation": "Improve TypeScript proficiency to write safer and more scalable code.",
        "category": "Programming Language",
    },
    "sql": {
        "recommendation": "Practice SQL queries and database design fundamentals.",
        "category": "Database",
    },
}

def generate_recommendations(missing_skills: List[str]) -> List[Dict[str, str]]:
    recommendations = []
    for skill in missing_skills:
        key = skill.lower()
        if key in SKILL_RECOMMENDATIONS:
            recommendations.append({
                "skill": skill,
                "recommendation": SKILL_RECOMMENDATIONS[key]["recommendation"],
                "category": SKILL_RECOMMENDATIONS[key]["category"],
            })
        else:
            recommendations.append({
                "skill": skill,
                "recommendation": f"Consider learning {skill} to enhance your skill set.",
                "category": "General",
            })
    return recommendations