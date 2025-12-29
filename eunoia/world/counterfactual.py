from typing import List
import copy

class CounterfactualSimulator:
    """
    Level 8.4 — Counterfactual Simulation

    Generates alternative reasoning strategies when:
    - expectations fail
    - retries stagnate
    - mutations underperform
    """

    def simulate(self, goal_description: str) -> List[str]:
        """
        Generate alternative goal reformulations.

        This is intentionally:
        - deterministic
        - structured
        - strategy-driven (not random)
        """

        goal = goal_description.lower()

        alternatives = []

        if "explain" in goal:
            core = goal.replace("explain", "").strip()
            alternatives.extend([
                f"Define {core}",
                f"Explain key components of {core}",
                f"Describe the process of {core}",
                f"Explain causes and effects of {core}",
            ])

        elif "compare" in goal:
            alternatives.append(f"Define both subjects in {goal}")
            alternatives.append(f"List similarities in {goal}")
            alternatives.append(f"List differences in {goal}")

        elif "why" in goal:
            alternatives.append(f"Explain underlying mechanisms of {goal}")
            alternatives.append(f"Describe causal chain in {goal}")

        else:
            alternatives.append(f"Break down {goal} into smaller parts")

        return alternatives

class CounterfactualEngine:
    def simulate(self, world_state, action):
        future = copy.deepcopy(world_state)
        future.update(action)
        return future