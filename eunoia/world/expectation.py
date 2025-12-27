from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Expectation:
    """
    Level 8.2 — Expected outcome of an action.
    """
    goal_id: int
    expected_properties: Dict[str, Any]
    confidence: float = 1.0


class ExpectationModel:
    """
    Unified Expectation Model

    Supports:
    - goal_id-based expectations (tests, controller)
    - goal_text-based expectations (world reasoning)
    """

    def __init__(self):
        # Goal-ID based expectations
        self._expectations_by_id: Dict[int, Expectation] = {}

        # Goal-text based expectations
        self._expectations_by_text: Dict[str, List[str]] = {}

    # ---------------------------
    # Goal-ID based API (tests)
    # ---------------------------

    def register(
        self,
        goal_id: int,
        expected_properties: Dict[str, Any],
        confidence: float = 1.0,
    ):
        self._expectations_by_id[goal_id] = Expectation(
            goal_id=goal_id,
            expected_properties=expected_properties,
            confidence=confidence,
        )

    def get(self, goal_id: int) -> Expectation | None:
        return self._expectations_by_id.get(goal_id)

    def clear(self, goal_id: int):
        if goal_id in self._expectations_by_id:
            del self._expectations_by_id[goal_id]

    # ---------------------------
    # Goal-text based API (world model)
    # ---------------------------

    def register_text(self, goal_text: str, required_facts: List[str]):
        self._expectations_by_text[goal_text.lower()] = required_facts

    def violated(self, goal_text: str, output: str) -> List[str]:
        missing = []
        reqs = self._expectations_by_text.get(goal_text.lower(), [])
        for r in reqs:
            if r.lower() not in output.lower():
                missing.append(r)
        return missing
