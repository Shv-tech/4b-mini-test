from eunoia.lmr.constraint_graph import ConstraintGraph
from eunoia.lmr.invariants import InvariantGuard


class VerificationError(Exception):
    pass


class LogicalVerifier:
    def __init__(
        self,
        constraints: ConstraintGraph,
        invariants: InvariantGuard
    ):
        self.constraints = constraints
        self.invariants = invariants

    def verify(self, values: dict):
        violations = self.constraints.evaluate(values)
        if violations:
            raise VerificationError(
                f"Constraint violations: {violations}"
            )

        self.invariants.enforce(values)
