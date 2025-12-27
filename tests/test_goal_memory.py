from eunoia.goals.goal_memory import GoalMemory


def test_goal_memory_recall():
    memory = GoalMemory()

    memory.record_success(
        "Explain photosynthesis",
        ["Explain chloroplasts", "Explain light reactions"],
    )

    recalled = memory.recall("Explain photosynthesis")

    assert recalled is not None
    assert "Explain chloroplasts" in recalled
    assert "Explain light reactions" in recalled
