import re
from typing import Dict, Set


class GoalEvaluator:
    """
    Lightweight semantic sufficiency evaluator.

    Designed to be:
    - strict for long goals
    - permissive for short semantic directives (e.g. 'Define X')
    """

    def _tokenize(self, text: str) -> Set[str]:
        cleaned = re.sub(r"[^a-z0-9\s]", "", text.lower())
        return set(cleaned.split())

    def evaluate(self, goal_text: str, output: str) -> Dict[str, bool]:
        # Empty or trivial output → retry
        if not output or len(output.strip()) < 20:
            return {"satisfied": False, "retry": True, "abandon": False}

        goal_keywords = self._tokenize(goal_text)
        output_keywords = self._tokenize(output)

        overlap = len(goal_keywords & output_keywords)

        # 🔥 CRITICAL FIX
        # Short goals like "Define photosynthesis" should not require 2 overlaps
        if len(goal_keywords) <= 2:
            required = 1
        else:
            required = max(2, len(goal_keywords) // 3)

        if overlap >= required:
            return {"satisfied": True, "retry": False, "abandon": False}

        return {"satisfied": False, "retry": True, "abandon": False}
