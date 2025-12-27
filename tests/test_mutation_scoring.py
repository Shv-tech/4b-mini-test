from eunoia.goals.goal_node import GoalNode
from eunoia.goals.goal_tree import GoalTree
from eunoia.goals.goal_controller import GoalController
from eunoia.goals.shared_state import GLOBAL_MUTATION_SCORE_STORE


def test_mutation_learning_is_shared_across_controllers():
    """
    Successful mutation strategy should transfer to new controllers.
    """

    # Reset shared mutation memory for test isolation
    GLOBAL_MUTATION_SCORE_STORE.reset()

    # ---------- First controller learns ----------
    root1 = GoalNode(1, "Explain photosynthesis", 1.0)
    tree1 = GoalTree(root1)
    controller1 = GoalController(tree1)

    goal1 = controller1.get_next_goal()

    # Trigger mutation
    controller1.on_step_complete(goal1, "bad")
    controller1.on_step_complete(goal1, "still bad")

    assert goal1.children, "Mutation did not generate children"

    # Provide a rich, correct answer
    rich_answer = (
        "Photosynthesis is defined as the biological process by which green plants, "
        "algae, and some bacteria use sunlight, carbon dioxide, and water to produce "
        "glucose and oxygen. This process occurs in chloroplasts and is essential "
        "for sustaining life on Earth."
    )

    # ✅ At least one mutation must succeed
    advanced = False
    for child in goal1.children:
        result = controller1.on_step_complete(child, rich_answer)
        if result == "ADVANCE":
            advanced = True
            break

    assert advanced, "No mutation child was accepted; evaluator may be too strict."

    # ---------- Second controller should reuse strategy ----------
    root2 = GoalNode(10, "Explain respiration", 1.0)
    tree2 = GoalTree(root2)
    controller2 = GoalController(tree2)

    goal2 = controller2.get_next_goal()
    controller2.on_step_complete(goal2, "bad")
    controller2.on_step_complete(goal2, "still bad")

    strategies = [c.description.lower() for c in goal2.children]

    # Learned strategies (like 'define') should appear
    assert any("define" in s for s in strategies), (
        "Learned mutation strategy was not reused in second controller."
    )
