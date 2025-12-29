from collections import defaultdict
from typing import Tuple, Dict


class AbstractionDetector:
    """
    Detects repeated reasoning signatures that should become tools.
    """

    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.pattern_counts: Dict[Tuple[str, ...], int] = defaultdict(int)

    def observe(self, signature: Tuple[str, ...]) -> bool:
        """
        Returns True if abstraction threshold is reached.
        """
        self.pattern_counts[signature] += 1
        return self.pattern_counts[signature] >= self.threshold