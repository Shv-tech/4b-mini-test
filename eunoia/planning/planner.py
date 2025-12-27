from typing import List
from eunoia.planning.plan_step import PlanStep
from eunoia.inference.base_model import BaseModel


class Planner:
    """
    Decomposes a high-level goal into ordered steps.
    """

    def __init__(self, model: BaseModel):
        self.model = model

    def create_plan(self, goal: str) -> List[PlanStep]:
        prompt = (
            "Decompose the following task into a numbered list of minimal, "
            "clear steps. Do not explain.\n\n"
            f"TASK:\n{goal}\n\n"
            "Steps:"
        )

        raw = self.model.generate(prompt)

        steps = []
        for i, line in enumerate(raw.splitlines()):
            if line.strip() and line[0].isdigit():
                steps.append(
                    PlanStep(
                        id=len(steps),
                        description=line.strip(),
                        constraints=[]
                    )
                )

        return steps
