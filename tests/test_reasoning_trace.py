from eunoia.meta.reasoning_trace import ReasoningTrace


def test_reasoning_trace_failure_rate():
    trace = ReasoningTrace()

    trace.record("Explain X", "initial", "RETRY", False)
    trace.record("Explain X", "mutation", "ADVANCE", True)

    assert trace.failure_rate() == 0.5
