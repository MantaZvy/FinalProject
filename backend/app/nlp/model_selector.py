from app.nlp.types import MatchResult

MODEL_PRIORITY = {
    "weighted_skill": 2,
    "keyword_overlap": 1,
}

def select_best_model(results: list[MatchResult]) -> MatchResult:
    if not results:
        raise ValueError("No NLP results to compare")

    return max(
        results,
        key=lambda r: (
            r["similarity_score"],
            MODEL_PRIORITY.get(r["model_name"], 0),
        ),
    )


