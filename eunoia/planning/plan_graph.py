from typing import List
from eunoia.planning.plan_step import PlanStep


class PlanGraph:
    def __init__(self, steps: List[PlanStep]):
        self.steps = steps

    def next_step(self):
        for step in self.steps:
            if not step.completed:
                return step
        return None

    def is_complete(self) -> bool:
        return all(step.completed for step in self.steps)
