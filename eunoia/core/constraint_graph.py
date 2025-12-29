# eunoia/core/constraint_graph.py

from typing import List, Any, Optional
import re


class ConstraintNode:
    """
    Atomic symbolic constraint with executable semantics.
    """

    def __init__(
        self,
        name: str,
        value: Any,
        priority: int = 0,
    ):
        self.name = name
        self.value = value
        self.priority = priority
        self.satisfied: bool = False

        # Stable identity
        self.signature: str = f"{self.name}:{self.value}"

    # --------------------------------------------------
    # ✅ REQUIRED BY ConstraintEvaluator
    # --------------------------------------------------
    def check(self, output: str) -> bool:
        """
        Evaluate this constraint against model output.
        """
        result = False

        if self.name == "steps":
            # Count numbered steps like "1." "2."
            steps = re.findall(r"^\s*\d+\.", output, flags=re.MULTILINE)
            result = len(steps) == int(self.value)

        elif self.name == "format":
            if self.value == "no_bullets":
                result = not bool(
                    re.search(r"^\s*[-*•]", output, flags=re.MULTILINE)
                )
            else:
                # Unknown format → pass (future-safe)
                result = True

        else:
            # Unknown constraint types are non-blocking by default
            result = True

        self.satisfied = result
        return result

    def __repr__(self) -> str:
        status = "✓" if self.satisfied else "✗"
        return f"<Constraint {self.signature} | {status}>"


class ConstraintGraph:
    """
    Backward-compatible constraint container.
    """

    def __init__(self):
        self.nodes: List[ConstraintNode] = []

    # ---------- Legacy + Modern API ----------
    def add_node(self, node: ConstraintNode):
        self.nodes.append(node)

    def add(self, node: ConstraintNode):
        self.nodes.append(node)

    def get_node(self, name: str) -> Optional[ConstraintNode]:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def all_constraints(self) -> List[ConstraintNode]:
        return list(self.nodes)

    # ---------- Helpers ----------
    def violations(self) -> List[ConstraintNode]:
        return sorted(
            (n for n in self.nodes if not n.satisfied),
            key=lambda n: n.priority,
            reverse=True,
        )

    def all_satisfied(self) -> bool:
        return all(n.satisfied for n in self.nodes)

    def __repr__(self) -> str:
        return f"<ConstraintGraph | {len(self.nodes)} constraints>"
