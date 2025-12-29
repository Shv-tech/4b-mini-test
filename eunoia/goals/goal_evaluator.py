import re
from typing import Dict, Set


INSTRUCTION_WORDS = {
    "define", "defined",
    "explain", "explained",
    "describe", "described",
    "example", "examples",
    "components", "component",
}


class GoalEvaluator:
    def _tokenize(self, text: str) -> Set[str]:
        cleaned = re.sub(r"[^a-z0-9\s]", "", text.lower())
        return set(cleaned.split())

    def evaluate(self, goal_text: str, output: str) -> Dict[str, bool]:
        # Empty or trivial output
        if not output or len(output.strip()) < 20:
            return {"satisfied": False, "retry": True, "abandon": False}

        goal_tokens = self._tokenize(goal_text)
        output_tokens = self._tokenize(output)

        # Separate instruction vs concept tokens
        concept_tokens = goal_tokens - INSTRUCTION_WORDS
        overlap = len(concept_tokens & output_tokens)

        # ---------- CRITICAL LHR LOGIC ----------
        # If concept is addressed, instruction verbs are irrelevant
        if concept_tokens:
            required = max(1, len(concept_tokens) // 2)
        else:
            required = 1

        if overlap >= required:
            return {"satisfied": True, "retry": False, "abandon": False}

        return {"satisfied": False, "retry": True, "abandon": False}
