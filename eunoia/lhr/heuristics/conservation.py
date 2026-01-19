# 🔥 FIX: Changed import path from 'lhr' to 'lmr'
from eunoia.lhr.heuristics.base import Heuristic

class ConservationHeuristic(Heuristic):
    name = "conservation"

    def apply(self, state):
        # Safety check: if inputs/outputs are missing, skip
        if not hasattr(state, 'inputs') or not hasattr(state, 'outputs'):
            return state

        total_in = sum(state.inputs)
        total_out = sum(state.outputs)
        
        # Default tolerance if not set
        tolerance = getattr(state, 'tolerance', 0.01)

        if abs(total_in - total_out) > tolerance:
            raise ValueError(f"Conservation violated: In({total_in}) != Out({total_out})")

        return state