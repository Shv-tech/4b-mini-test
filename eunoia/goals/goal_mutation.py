from eunoia.goals.goal_node import GoalNode
from eunoia.goals.shared_state import GLOBAL_MUTATION_SCORE_STORE


class GoalMutationEngine:
    """
    Generates mutated child goals.
    Uses global mutation learning to bias strategy choice.
    """

    BASE_MUTATIONS = [
        "Define",
        "Explain components of",
        "Describe the process of",
    ]

    def mutate(self, goal: GoalNode):
        base_text = goal.description.lower()

        # 🔥 Rank strategies by learned success
        ranked = GLOBAL_MUTATION_SCORE_STORE.ranked(self.BASE_MUTATIONS)

        for strategy in ranked:
            desc = f"{strategy} {base_text}"
            child = GoalNode(
                goal_id=goal.goal_id * 10 + len(goal.children) + 1,
                description=desc,
                priority=min(goal.priority + 0.2, 1.0),
                parent=goal,
            )
            child._mutation_strategy = strategy.lower()
            goal.add_child(child)
