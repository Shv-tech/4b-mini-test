from eunoia.lhr.heuristics.conservation import ConservationHeuristic
from eunoia.lhr.heuristics.causality import CausalityHeuristic
from eunoia.lhr.heuristics.boundary import BoundaryHeuristic
from eunoia.lhr.heuristics.oom import OrderOfMagnitudeHeuristic


class LogicalCPU:
    def __init__(self):
        self.heuristics = [
            ConservationHeuristic(),
            CausalityHeuristic(),
            BoundaryHeuristic(),
            OrderOfMagnitudeHeuristic(),
        ]

    def execute(self, state):
        for h in self.heuristics:
            state = h.apply(state)
        return state
