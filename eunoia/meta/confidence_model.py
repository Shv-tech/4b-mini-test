class ConfidenceModel:
    def compute(self, rts, verification_results):
        score = 1.0

        # Penalize missing structure
        if not rts.get("constraints"):
            score -= 0.15

        if not rts.get("variables"):
            score -= 0.15

        # Penalize disagreement
        if not verification_results["agreement"]:
            score -= 0.3

        # Penalize invariant stress
        score -= verification_results.get("invariant_penalty", 0)

        return max(0.0, min(score, 1.0))
