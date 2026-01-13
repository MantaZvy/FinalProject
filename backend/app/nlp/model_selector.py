from app.nlp.types import MatchResult

def select_best_model(results: list[MatchResult]) -> MatchResult:
    """
    Simple rule-based selector:
    - Highest similarity_score wins
    """
    if not results:
        raise ValueError("No NLP results to compare")

    return max(results, key=lambda r: r["similarity_score"])


