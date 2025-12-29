from typing import Optional

from eunoia.goals.goal_node import GoalNode
from eunoia.goals.goal_tree import GoalTree
from eunoia.goals.goal_evaluator import GoalEvaluator
from eunoia.goals.execution_gate import ExecutionGate
from eunoia.goals.goal_mutation import GoalMutationEngine
from eunoia.goals.goal_memory import GoalMemory
from eunoia.goals.strategy_memory import StrategyMemory
from eunoia.goals.shared_state import GLOBAL_MUTATION_SCORE_STORE

from eunoia.meta.reasoning_trace import ReasoningTrace
from eunoia.meta.outcome_scorer import OutcomeScorer
from eunoia.meta.meta_controller import MetaController


class GoalController:
    def __init__(
        self,
        goal_tree: GoalTree,
        evaluator: GoalEvaluator | None = None,
        gate: ExecutionGate | None = None,
        mutation_engine: GoalMutationEngine | None = None,
        strategy_memory: StrategyMemory | None = None,
        goal_memory: GoalMemory | None = None,
        meta_controller: MetaController | None = None,
        trace: ReasoningTrace | None = None,
        outcome_scorer: OutcomeScorer | None = None,
    ):
        self.goal_tree = goal_tree
        self.evaluator = evaluator or GoalEvaluator()
        self.gate = gate or ExecutionGate(max_retries=2)

        self.mutation_scores = GLOBAL_MUTATION_SCORE_STORE
        self.mutation_engine = mutation_engine or GoalMutationEngine()

        self.strategy_memory = strategy_memory or StrategyMemory()
        self.goal_memory = goal_memory or GoalMemory()

        self.trace = trace or ReasoningTrace()
        self.outcome_scorer = outcome_scorer or OutcomeScorer()
        self.meta_controller = meta_controller or MetaController(
            mutation_engine=self.mutation_engine,
            strategy_memory=self.strategy_memory,
        )

        self._retry_counter: dict[int, int] = {}

    def get_next_goal(self) -> Optional[GoalNode]:
        goal = self.goal_tree.get_next_goal()
        if not goal:
            return None

        abstracted = self.strategy_memory.recall(goal.description)
        if abstracted and not goal.children:
            for desc in abstracted:
                GoalNode(
                    goal_id=self.goal_tree.next_id(),
                    description=desc,
                    priority=min(goal.priority + 0.3, 1.0),
                    parent=goal,
                    tree=self.goal_tree,
                )

        return goal

    def on_step_complete(self, goal: GoalNode, output: str) -> str:
        gid = goal.goal_id
        self._retry_counter.setdefault(gid, 0)

        eval_result = self.evaluator.evaluate(goal.description, output)
        decision = self.gate.decide(eval_result, self._retry_counter[gid])

        self.trace.record(
            goal.description,
            action="step",
            decision=decision,
            success=(decision == "ADVANCE"),
        )

        score = self.outcome_scorer.score(self.trace)
        self.meta_controller.adapt(self.trace, score)
        self.trace.reset()

        if decision == "ADVANCE":
            if hasattr(goal, "_mutation_strategy"):
                self.mutation_scores.record_success(goal._mutation_strategy)

            self.goal_tree.mark_goal_satisfied(goal)
            self._retry_counter.pop(gid, None)

            if goal.children:
                children = [c.description for c in goal.children]
                self.goal_memory.record_success(goal.description, children)
                self.strategy_memory.record_strategy(goal.description, children)

            return "ADVANCE"

        if decision == "RETRY":
            self._retry_counter[gid] += 1
            if self._retry_counter[gid] >= self.gate.max_retries:
                self.mutation_engine.mutate(goal)
            return "RETRY"

        if decision == "ABANDON":
            if hasattr(goal, "_mutation_strategy"):
                self.mutation_scores.record_failure(goal._mutation_strategy)
            goal.abandon()
            self._retry_counter.pop(gid, None)
            return "ABANDON"

        return "RETRY"
