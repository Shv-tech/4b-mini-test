from collections import defaultdict


class MutationScoreStore:
    """
    Tracks success/failure statistics for mutation strategies.
    Shared globally.
    """

    def __init__(self):
        self.stats = defaultdict(lambda: {"success": 0, "fail": 0})

    def record_success(self, strategy: str):
        self.stats[strategy]["success"] += 1

    def record_failure(self, strategy: str):
        self.stats[strategy]["fail"] += 1

    def score(self, strategy: str) -> float:
        s = self.stats[strategy]
        total = s["success"] + s["fail"]
        if total == 0:
            return 0.0
        return s["success"] / total

    def ranked(self, strategies: list[str]) -> list[str]:
        """
        Return strategies ranked by past success.
        """
        return sorted(
            strategies,
            key=lambda s: self.score(s),
            reverse=True
        )

    def reset(self):
        self.stats.clear()
