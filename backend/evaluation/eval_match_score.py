#Evaluation 3: Match Score Validation. Tests the hybrid TF-IDF match scoring model across different resume-job pair scenarios.


import re, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#normalisation helpers
ALIASES = {
    'js':'javascript','ts':'typescript','py':'python',
    'reactjs':'react','nodejs':'node','postgres':'postgresql',
    'fast-api':'fastapi'
}

def normalize_skills(raw):
    normalized = set()
    for item in raw:
        parts = re.split(r'[,\n/()]+|\s+', item)
        for part in parts:
            token = part.lower().strip()
            token = re.sub(r'[^a-z0-9+#]', '', token)
            if token:
                normalized.add(ALIASES.get(token, token))
    return normalized

def tfidf_match(resume, job):
    def build_resume_text(r):
        parts = []
        for s in r.get('skills', []): parts.extend([s.lower()] * 3)
        parts.extend([k.lower() for k in r.get('keywords', [])])
        for exp in r.get('experience', []):
            if isinstance(exp, dict):
                text = f"{exp.get('role','')} {exp.get('company','')} {exp.get('description','')}".lower()
                parts.extend([text] * 2)
        return ' '.join(parts)

    def build_job_text(j):
        parts = [j.get('title', '').lower()] * 2
        parts.append(j.get('description', '').lower())
        for s in j.get('skills', []): parts.extend([s.lower()] * 3)
        return ' '.join(parts)

    rt = build_resume_text(resume)
    jt = build_job_text(job)
    if not rt.strip() or not jt.strip():
        return 0.0
    vec = TfidfVectorizer(ngram_range=(1,2), stop_words='english', min_df=1, sublinear_tf=True)
    m = vec.fit_transform([rt, jt])
    return float(cosine_similarity(m[0:1], m[1:2])[0][0])

def final_match(resume, job):
    rs = normalize_skills(resume.get('skills', []) + resume.get('keywords', []))
    js = normalize_skills(job.get('skills', []))
    matched = sorted(rs & js)
    missing = sorted(js - rs)
    skill_score = min(len(matched) / len(js) * 1.25, 1.0) if js else 0
    tfidf_score = tfidf_match(resume, job)
    final_score = round(0.6 * tfidf_score + 0.3 * skill_score, 3)
    return {
        'similarity_score': final_score,
        'matched_skills': matched,
        'missing_skills': missing,
        'tfidf_score': round(tfidf_score, 3),
        'skill_score': round(skill_score, 3),
    }
    
TEST_PAIRS = [
    {
        "name": "Strong Python match",
        "expected_rank": 1,
        "resume": {
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy", "docker", "rest"],
            "keywords": ["python", "fastapi", "postgresql", "backend", "api"],
            "experience": [{"role": "Backend Developer", "company": "TechCorp",
                            "description": "Built FastAPI microservices with PostgreSQL and SQLAlchemy"}]
        },
        "job": {
            "title": "Python Backend Developer",
            "description": "Python developer experienced with FastAPI and PostgreSQL for backend services",
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy"],
            "keywords": ["python", "backend", "api", "postgresql"]
        }
    },
    {
        "name": "Partial skills match",
        "expected_rank": 2,
        "resume": {
            "skills": ["python", "javascript", "react"],
            "keywords": ["python", "web", "frontend"],
            "experience": [{"role": "Junior Developer", "company": "Agency",
                            "description": "Built web applications using Python and React"}]
        },
        "job": {
            "title": "Python Backend Developer",
            "description": "Python developer experienced with FastAPI and PostgreSQL for backend services",
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy"],
            "keywords": ["python", "backend", "api", "postgresql"]
        }
    },
    {
        "name": "Low match — hospitality",
        "expected_rank": 3,
        "resume": {
            "skills": ["customer service", "excel", "communication", "teamwork"],
            "keywords": ["hospitality", "service", "teamwork"],
            "experience": [{"role": "Team Member", "company": "Restaurant",
                            "description": "Customer service and hospitality work in fast-paced environment"}]
        },
        "job": {
            "title": "Python Backend Developer",
            "description": "Python developer experienced with FastAPI and PostgreSQL for backend services",
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy"],
            "keywords": ["python", "backend", "api", "postgresql"]
        }
    },
    {
        "name": "Frontend role mismatch",
        "expected_rank": 4,
        "resume": {
            "skills": ["react", "javascript", "typescript", "css", "html"],
            "keywords": ["frontend", "react", "javascript", "ui"],
            "experience": [{"role": "Frontend Developer", "company": "Startup",
                            "description": "Built React applications with TypeScript and CSS"}]
        },
        "job": {
            "title": "Python Backend Developer",
            "description": "Python developer experienced with FastAPI and PostgreSQL for backend services",
            "skills": ["python", "fastapi", "postgresql", "sqlalchemy"],
            "keywords": ["python", "backend", "api", "postgresql"]
        }
    },
]


def run():
    print("\n" + "="*65)
    print("MATCH SCORE VALIDATION — EVALUATION RESULTS")
    print("="*65)

    results = []
    for pair in TEST_PAIRS:
        r = final_match(pair["resume"], pair["job"])
        results.append({
            "name": pair["name"],
            "score": r["similarity_score"],
            "tfidf": r["tfidf_score"],
            "skill": r["skill_score"],
            "matched": r["matched_skills"],
            "missing": r["missing_skills"],
            "expected_rank": pair["expected_rank"],
        })
        print(f"\n  {pair['name']}")
        print(f"    Similarity Score: {r['similarity_score']:.3f} ({r['similarity_score']*100:.1f}%)")
        print(f"    TF-IDF Score:     {r['tfidf_score']:.3f}")
        print(f"    Skill Score:      {r['skill_score']:.3f}")
        print(f"    Matched Skills:   {r['matched_skills']}")
        print(f"    Missing Skills:   {r['missing_skills']}")

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    actual_ranks = {r["name"]: i+1 for i, r in enumerate(sorted_results)}

    print(f"\n{'='*65}")
    print("RANKING VALIDATION")
    print(f"{'='*65}")
    ranking_correct = 0
    for res in results:
        actual = actual_ranks[res["name"]]
        expected = res["expected_rank"]
        correct = actual == expected
        if correct:
            ranking_correct += 1
        status = "CORRECT" if correct else f"MISMATCH (expected {expected}, got {actual})"
        print(f"  {res['name'][:38]:<38} Rank {actual} — {status}")

    ranking_acc = ranking_correct / len(results)
    scores = [r["score"] for r in results]
    print(f"\n  Ranking Accuracy: {ranking_acc:.1%}")
    print(f"  Score range:      {min(scores):.3f} – {max(scores):.3f}")
    print(f"  Score spread:     {(max(scores)-min(scores)):.3f}")
    print("="*65)

    return results


def plot_results(results):
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        names = [r["name"] for r in results]
        scores = [r["score"] * 100 for r in results]
        tfidf_scores = [r["tfidf"] * 100 for r in results]
        skill_scores = [r["skill"] * 100 for r in results]
        colors = ['#22c55e', '#f59e0b', '#ef4444', '#ef4444']

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Match Score Validation Results', fontsize=14, fontweight='bold')

        #chart 1 — horizontal bar chart of final similarity scores
        y_pos = np.arange(len(names))
        bars = axes[0].barh(y_pos, scores, color=colors, edgecolor='white', height=0.5)

        for bar, score in zip(bars, scores):
            axes[0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{score:.1f}%', va='center', ha='left', fontsize=10, fontweight='bold')

        short_names = ["Strong Python", "Partial match", "Hospitality", "Frontend"]
        axes[0].set_yticks(y_pos)
        axes[0].set_yticklabels(short_names, fontsize=10)
        axes[0].set_xlim(0, 90)
        axes[0].set_xlabel('Similarity Score (%)')
        axes[0].set_title('Final Similarity Score per Resume-Job Pair')
        axes[0].set_facecolor('#f9fafb')
        axes[0].axvline(x=50, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='50% threshold')
        axes[0].legend(fontsize=9)

        #chart 2 — grouped bar showing TF-IDF vs skill score breakdown
        x = np.arange(len(names))
        width = 0.35
        bars1 = axes[1].bar(x - width/2, tfidf_scores, width,
                            label='TF-IDF score (60% weight)',
                            color='#3b82f6', edgecolor='white')
        bars2 = axes[1].bar(x + width/2, skill_scores, width,
                            label='Skill score (30% weight)',
                            color='#a78bfa', edgecolor='white')

        for bar in bars1:
            h = bar.get_height()
            if h > 0:
                axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.5,
                            f'{h:.1f}%', ha='center', va='bottom', fontsize=8)
        for bar in bars2:
            h = bar.get_height()
            if h > 0:
                axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.5,
                            f'{h:.1f}%', ha='center', va='bottom', fontsize=8)

        axes[1].set_xticks(x)
        axes[1].set_xticklabels(short_names, fontsize=9)
        axes[1].set_ylabel('Score (%)')
        axes[1].set_title('TF-IDF vs Skill Score Breakdown')
        axes[1].legend(fontsize=9)
        axes[1].set_facecolor('#f9fafb')

        plt.tight_layout()
        output_path = 'evaluation/match_score_results.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\nGraph saved to: {output_path}")
        plt.show()

    except ImportError:
        print("\nInstall matplotlib: pip install matplotlib")


if __name__ == "__main__":
    results = run()
    plot_results(results)