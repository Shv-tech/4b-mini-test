class EscalationController:
    def escalate(self, rts):
        rts["heuristics_used"].append("boundary_conditions")
        rts["heuristics_used"].append("order_of_magnitude")
        rts["confidence"] *= 0.9
        return rts