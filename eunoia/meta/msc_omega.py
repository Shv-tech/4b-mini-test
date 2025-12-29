from eunoia.meta.confidence_model import ConfidenceModel
from eunoia.meta.decision_governor import DecisionGovernor
from eunoia.meta.escalation import EscalationController


class MSComega:
    def __init__(self):
        self.confidence = ConfidenceModel()
        self.decision = DecisionGovernor()
        self.escalation = EscalationController()

    def judge(self, rts, verification_results):
        confidence = self.confidence.compute(rts, verification_results)
        action = self.decision.decide(confidence, rts)

        if action == "ESCALATE":
            rts = self.escalation.escalate(rts)

        return {
            "action": action,
            "confidence": confidence,
            "rts": rts
        }