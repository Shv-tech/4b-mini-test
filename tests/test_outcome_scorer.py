from eunoia.meta.reasoning_trace import ReasoningTrace
from eunoia.meta.outcome_scorer import OutcomeScorer


def test_outcome_scoring():
    trace = ReasoningTrace()
    scorer = OutcomeScorer()

    trace.record("G", "a", "RETRY", False)
    trace.record("G", "b", "ADVANCE", True)

    score = scorer.score(trace)
    assert 0.5 < score <= 1.0
