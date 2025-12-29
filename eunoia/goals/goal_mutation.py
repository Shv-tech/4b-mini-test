from eunoia.goals.goal_node import GoalNode
from eunoia.goals.shared_state import GLOBAL_MUTATION_SCORE_STORE


class GoalMutationEngine:
    """
    Generates sub-goals when a goal fails repeatedly.
    """

    def __init__(self):
        self.score_store = GLOBAL_MUTATION_SCORE_STORE
        self.exploration_bias = 1.0
        self.max_children = 3

    def increase_exploration(self):
        self.exploration_bias = min(self.exploration_bias + 0.2, 2.0)

    def decrease_exploration(self):
        self.exploration_bias = max(self.exploration_bias - 0.1, 0.5)

    def mutate(self, goal: GoalNode):
        strategies = self.score_store.best_strategies()

        if not strategies:
            strategies = [
                "Define " + goal.description,
                "Explain components of " + goal.description,
                "Give an example of " + goal.description,
            ]

        limit = int(self.max_children * self.exploration_bias)
        limit = max(1, min(limit, 5))

        for strategy in strategies[:limit]:
            child = GoalNode(
                goal_id=goal.tree.next_id(),
                description=strategy,
                priority=min(goal.priority + 0.2, 1.0),
                parent=goal,
                tree=goal.tree,
            )
            child._mutation_strategy = strategy
