from eunoia.goals.goal_node import GoalNode
from eunoia.goals.goal_tree import GoalTree
from eunoia.goals.goal_evaluator import GoalEvaluator
from eunoia.goals.execution_gate import ExecutionGate
from eunoia.goals.goal_mutation import GoalMutationEngine
from eunoia.goals.goal_controller import GoalController


def build_controller():
    root = GoalNode(0, "Explain photosynthesis", priority=1.0)
    tree = GoalTree(root)

    controller = GoalController(
        goal_tree=tree,
        evaluator=GoalEvaluator(),
        gate=ExecutionGate(max_retries=2),
        mutation_engine=GoalMutationEngine(),
    )

    return controller, tree, root

