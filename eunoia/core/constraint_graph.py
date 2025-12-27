from dataclasses import dataclass, field
from typing import Dict, Any, List


# ----------------------------
# Constraint Node
# ----------------------------

@dataclass
class ConstraintNode:
    name: str
    value: Any
    priority: int
    satisfied: bool = False

    def check(self, output: str) -> bool:
        from eunoia.core.constraint_graph import ConstraintChecks

        if self.name == "steps":
            self.satisfied = ConstraintChecks.check_steps(self.value, output)

        elif self.name == "format" and self.value == "no_bullets":
            self.satisfied = ConstraintChecks.check_no_bullets(output)

        elif self.name == "tone":
            self.satisfied = ConstraintChecks.check_tone(self.value, output)

        else:
            self.satisfied = True  # unknown constraints default to pass

        return self.satisfied


# ----------------------------
# Constraint Graph
# ----------------------------

@dataclass
class ConstraintGraph:
    nodes: Dict[str, ConstraintNode] = field(default_factory=dict)

    def add_node(self, node: ConstraintNode):
        self.nodes[node.name] = node

    def get_node(self, name: str) -> ConstraintNode:
        return self.nodes.get(name)

    def all_constraints(self) -> List[ConstraintNode]:
        return list(self.nodes.values())

    def unsatisfied(self) -> List[ConstraintNode]:
        return [n for n in self.nodes.values() if not n.satisfied]


# ----------------------------
# Constraint Checks
# ----------------------------

class ConstraintChecks:
    @staticmethod
    def check_steps(value: int, output: str) -> bool:
        steps = sum(
            1
            for line in output.splitlines()
            if line.strip().startswith(tuple(f"{i}." for i in range(1, value + 1)))
        )
        return steps == value

    @staticmethod
    def check_no_bullets(output: str) -> bool:
        bullet_markers = ("-", "*", "•")
        return not any(
            line.strip().startswith(bullet_markers)
            for line in output.splitlines()
        )

    @staticmethod
    def check_tone(value: str, output: str) -> bool:
        calm_words = {"please", "gently", "calm", "smooth", "soft"}
        if value == "calm":
            return any(w in output.lower() for w in calm_words)
        return True
