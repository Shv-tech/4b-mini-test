class EscalationRequired(Exception):
    pass


class EscalationController:
    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts

    def handle_failure(self, attempt):
        if attempt >= self.max_attempts:
            raise EscalationRequired(
                "Cannot reach stable answer after escalation"
            )
