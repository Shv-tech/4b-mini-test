class OrderOfMagnitudeHeuristic(Heuristic):
    name = "order_of_magnitude"

    def apply(self, state):
        if state.estimated and state.calculated:
            ratio = state.calculated / state.estimated
            if ratio > 10 or ratio < 0.1:
                raise ValueError("OOM mismatch")
        return state