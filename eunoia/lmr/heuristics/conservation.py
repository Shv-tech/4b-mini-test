from eunoia.lhr.heuristics.base import Heuristic


class ConservationHeuristic(Heuristic):
    name = "conservation"

    def apply(self, state):
        total_in = sum(state.inputs)
        total_out = sum(state.outputs)

        if abs(total_in - total_out) > state.tolerance:
            raise ValueError("Conservation violated")

        return state