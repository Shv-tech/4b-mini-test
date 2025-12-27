class OutcomeScorer:
    """
    Scores reasoning quality across a trace.
    """

    def score(self, trace) -> float:
        """
        Score ∈ [0, 1]
        """
        if not trace.steps:
            return 0.0

        success_weight = sum(
            1.0 if s.success else 0.3
            for s in trace.steps
        )

        return success_weight / len(trace.steps)
