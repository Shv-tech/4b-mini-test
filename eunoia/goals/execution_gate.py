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
        """
        Decision priority order (non-negotiable):

        1. SATISFIED  -> ADVANCE
        2. ABANDON    -> ABANDON
        3. RETRY     -> while retries remain
        4. ABANDON   -> when retries exhausted
        """

        # ✅ Absolute override — satisfaction wins
        if eval_result.get("satisfied", False):
            return "ADVANCE"

        # Explicit abandon signal
        if eval_result.get("abandon", False):
            return "ABANDON"

        # Retry budget only applies if NOT satisfied
        if retries < self.max_retries:
            return "RETRY"

        return "ABANDON"
