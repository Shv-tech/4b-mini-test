class CausalityHeuristic(Heuristic):
    name = "causality"

    def apply(self, state):
        for effect in state.effects:
            if effect not in state.causes:
                raise ValueError("Uncaused effect detected")
        return state