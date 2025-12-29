class ExecutionGate:
    """
    Decides whether to ADVANCE, RETRY, or ABANDON a goal.

    CRITICAL INVARIANT:
    - If a goal is SATISFIED, it MUST ADVANCE immediately.
    - Retry logic is ONLY for unsatisfied goals.
    """

    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    def decide(self, eval_result: dict, retries: int) -> str:
        # Absolute override
        if eval_result.get("satisfied", False):
            return "ADVANCE"

        if eval_result.get("abandon", False):
            return "ABANDON"

        if retries < self.max_retries:
            return "RETRY"

        return "ABANDON"
