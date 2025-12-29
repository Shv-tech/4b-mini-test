class BoundaryHeuristic(Heuristic):
    name = "boundary"

    def apply(self, state):
        for v in state.variables.values():
            if v < state.min_allowed or v > state.max_allowed:
                raise ValueError("Boundary violation")
        return state