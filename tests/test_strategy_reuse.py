from eunoia.goals.strategy_memory import StrategyMemory


def test_strategy_abstraction_reuse():
    memory = StrategyMemory()

    memory.record_strategy(
        "Explain photosynthesis",
        [
            "Define photosynthesis",
            "Explain components of photosynthesis",
            "Explain process of photosynthesis",
        ],
    )

    reused = memory.recall("Explain gravity")

    assert reused is not None
    assert any("define gravity" in r.lower() for r in reused)
    assert any("components of gravity" in r.lower() or "process of gravity" in r.lower() for r in reused)
