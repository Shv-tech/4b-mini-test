from dataclasses import dataclass
from typing import Dict, List
import re


STOPWORDS = {"explain", "describe", "what", "is", "of", "the", "a", "an"}


def extract_concept(goal_text: str) -> str:
    """
    Extract the main concept noun from a goal.
    """
    text = goal_text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = [t for t in text.split() if t not in STOPWORDS]
    return tokens[-1] if tokens else ""


@dataclass
class StrategyPattern:
    name: str
    trigger: str
    templates: List[str]
    success_count: int = 1


class StrategyMemory:
    """
    Level 7.4: Cross-goal abstraction reuse
    """

    def __init__(self):
        self.strategies: Dict[str, StrategyPattern] = {}

    def record_strategy(self, parent_goal: str, child_goals: List[str]):
        parent = parent_goal.lower()

        if "explain" in parent:
            trigger = "explain"
            name = "EXPLAIN_CONCEPT"
        else:
            return

        parent_concept = extract_concept(parent_goal)
        templates = []

        for child in child_goals:
            child_lower = child.lower()
            if parent_concept in child_lower:
                template = child_lower.replace(parent_concept, "{X}")
                templates.append(template)

        if not templates:
            return

        if name in self.strategies:
            self.strategies[name].success_count += 1
        else:
            self.strategies[name] = StrategyPattern(
                name=name,
                trigger=trigger,
                templates=templates,
            )

    def recall(self, goal_text: str) -> List[str] | None:
        goal = goal_text.lower()
        concept = extract_concept(goal_text)

        for strat in self.strategies.values():
            if strat.trigger in goal:
                return [t.replace("{X}", concept) for t in strat.templates]

        return None
