from dataclasses import dataclass
from typing import List


@dataclass
class ReasoningStep:
    goal: str
    action: str
    decision: str
    success: bool


class ReasoningTrace:
    """
    Records reasoning steps for meta-analysis.
    """

    def __init__(self):
        self.steps: List[ReasoningStep] = []

    def record(
        self,
        goal: str,
        action: str,
        decision: str,
        success: bool,
    ):
        self.steps.append(
            ReasoningStep(goal, action, decision, success)
        )

    def failure_rate(self) -> float:
        if not self.steps:
            return 0.0
        failures = sum(1 for s in self.steps if not s.success)
        return failures / len(self.steps)

    def reset(self):
        self.steps.clear()
