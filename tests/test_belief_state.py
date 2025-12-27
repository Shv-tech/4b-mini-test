from eunoia.world.belief_state import BeliefState


def test_belief_state_basic_operations():
    beliefs = BeliefState()

    beliefs.set("goal_active", True)
    beliefs.set("domain", "biology")

    assert beliefs.get("goal_active") is True
    assert beliefs.get("domain") == "biology"

    beliefs.revise("goal_active", False)
    assert beliefs.get("goal_active") is False

    beliefs.update({"confidence": 0.9})
    assert beliefs.get("confidence") == 0.9

    snapshot = beliefs.snapshot()
    assert snapshot["domain"] == "biology"
