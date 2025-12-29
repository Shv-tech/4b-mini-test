from collections import Counter


class ArbitrationFailure(Exception):
    pass


class AnswerArbiter:
    def __init__(self, tolerance=1e-6):
        self.tolerance = tolerance

    def _normalize(self, x):
        if isinstance(x, float):
            return round(x, 6)
        return x

    def arbitrate(self, outputs):
        answers = [self._normalize(o.answer) for o in outputs]

        counts = Counter(answers)
        winner, count = counts.most_common(1)[0]

        if count < 2:
            raise ArbitrationFailure(
                f"No consensus among solvers: {answers}"
            )

        return winner
