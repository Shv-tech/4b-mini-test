from eunoia.lhr.solvers import (
    AlgebraicSolver,
    NumericSolver,
    LinguisticSolver,
)
from eunoia.lhr.arbiter import AnswerArbiter, ArbitrationFailure
from eunoia.lhr.escalation import EscalationController


class SSCOmega:
    def __init__(self):
        self.solvers = [
            AlgebraicSolver(),
            NumericSolver(),
            LinguisticSolver(),
        ]
        self.arbiter = AnswerArbiter()
        self.escalation = EscalationController()

    def solve(self, problem, rts):
        attempt = 0
        while True:
            attempt += 1

            outputs = [s.solve(problem, rts) for s in self.solvers]

            try:
                return self.arbiter.arbitrate(outputs)
            except ArbitrationFailure:
                self.escalation.handle_failure(attempt)
