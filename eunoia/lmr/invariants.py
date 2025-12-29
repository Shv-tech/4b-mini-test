from typing import Dict, Callable


class InvariantViolation(Exception):
    pass


class Invariant:
    def __init__(self, name: str, check: Callable[[Dict[str, float]], bool]):
        self.name = name
        self.check = check


class InvariantGuard:
    """
    Hard invariants that must NEVER be broken.
    """

    def __init__(self):
        self.invariants = []

    def register(self, invariant: Invariant):
        self.invariants.append(invariant)

    def enforce(self, values: Dict[str, float]):
        for inv in self.invariants:
            if not inv.check(values):
                raise InvariantViolation(
                    f"Invariant violated: {inv.name}"
                )
