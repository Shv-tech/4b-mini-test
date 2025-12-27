"""
Global cognitive substrate shared across all GoalControllers.
"""

from eunoia.goals.mutation_scoring import MutationScoreStore

# 🔥 Shared across all agents / controllers
GLOBAL_MUTATION_SCORE_STORE = MutationScoreStore()
