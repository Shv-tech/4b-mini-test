from eunoia.lhr.reasoning_modes import ReasoningMode


class SolverOutput:
    def __init__(self, answer, values, confidence):
        self.answer = answer
        self.values = values
        self.confidence = confidence


class BaseSolver:
    mode: ReasoningMode

    def solve(self, problem, rts):
        raise NotImplementedError


class AlgebraicSolver(BaseSolver):
    mode = ReasoningMode.ALGEBRAIC

    def solve(self, problem, rts):
        # symbolic variable solving
        values = rts["variables"]
        answer = values.get("result")
        return SolverOutput(answer, values, confidence=0.95)


class NumericSolver(BaseSolver):
    mode = ReasoningMode.NUMERIC

    def solve(self, problem, rts):
        values = rts["variables"]
        answer = sum(v for v in values.values() if isinstance(v, (int, float)))
        return SolverOutput(answer, values, confidence=0.90)


class LinguisticSolver(BaseSolver):
    mode = ReasoningMode.LINGUISTIC

    def solve(self, problem, rts):
        answer = rts.get("final_guess")
        return SolverOutput(answer, rts["variables"], confidence=0.75)
