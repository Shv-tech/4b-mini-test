from typing import List
from eunoia.core.constraint_graph import ConstraintGraph, ConstraintNode


class ConstraintEvaluator:
    def evaluate(self, graph: ConstraintGraph, output: str):
        violations: List[ConstraintNode] = []

        for node in graph.all_constraints():
            if not node.check(output):
                violations.append(node)

        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
        }
