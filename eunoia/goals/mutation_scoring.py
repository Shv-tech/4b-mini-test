from collections import defaultdict
from typing import List


class MutationScoreStore:
    """
    Global shared memory of how well mutation strategies perform.
    """

    def __init__(self):
        self.stats = defaultdict(lambda: {"success": 0, "fail": 0})

    def record_success(self, strategy: str):
        self.stats[strategy]["success"] += 1

    def record_failure(self, strategy: str):
        self.stats[strategy]["fail"] += 1

    def best_strategies(self, limit: int = 3) -> List[str]:
        if not self.stats:
            return []

        scored = []
        for strategy, data in self.stats.items():
            success = data["success"]
            fail = data["fail"]
            score = (success + 1) / (success + fail + 2)
            scored.append((score, strategy))

        scored.sort(reverse=True)
        return [s for _, s in scored[:limit]]

    def reset(self):
        self.stats.clear()
