class DummyMutationEngine:
    def __init__(self):
        self.mode = "balanced"

    def increase_exploration(self):
        self.mode = "explore"

    def decrease_exploration(self):
        self.mode = "exploit"


from eunoia.meta.meta_controller import MetaController
from eunoia.meta.reasoning_trace import ReasoningTrace


def test_meta_controller_adaptation():
    engine = DummyMutationEngine()
    meta = MetaController(engine, None)

    trace = ReasoningTrace()
    trace.record("X", "a", "RETRY", False)

    meta.adapt(trace, score=0.2)
    assert engine.mode == "explore"

    meta.adapt(trace, score=0.9)
    assert engine.mode == "exploit"
