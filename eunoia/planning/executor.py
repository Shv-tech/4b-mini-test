from eunoia.inference.eunoia_loop import EunoiaController
from eunoia.planning.plan_graph import PlanGraph


class PlanExecutor:
    """
    Executes a plan step-by-step using Eunoia control.
    """

    def __init__(self, controller: EunoiaController):
        self.controller = controller

    def execute(self, plan: PlanGraph):
        execution_log = []

        while not plan.is_complete():
            step = plan.next_step()
            if step is None:
                break

            result = self.controller.run(step.description)

            step.output = result["final_output"]
            step.completed = True

            execution_log.append({
                "step_id": step.id,
                "description": step.description,
                "output": step.output,
                "iterations": result["iterations"],
                "memory_hit": result["memory_hit"],
            })

        return execution_log
