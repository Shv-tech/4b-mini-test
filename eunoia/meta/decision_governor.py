class DecisionGovernor:
    def decide(self, confidence, context):
        if confidence >= 0.85:
            return "ANSWER"

        if 0.6 <= confidence < 0.85:
            return "ESCALATE"

        return "ABSTAIN"