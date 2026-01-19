# 🔥 FIX: Import the base class!
from eunoia.lhr.heuristics.base import Heuristic

class CausalityHeuristic(Heuristic):
    name = "causality"

    def apply(self, state):
        # Safety check for missing attributes
        if not hasattr(state, 'effects') or not hasattr(state, 'causes'):
            return state

        for effect in state.effects:
            if effect not in state.causes:
                raise ValueError(f"Causality Violation: Effect '{effect}' occurs without cause.")
        return state