from dataclasses import dataclass
from typing import Dict, Set, List


@dataclass
class VariableNode:
    name: str
    value: float | None = None
    unit: str | None = None


class VariableGraph:
    """
    Explicit Variable–Entity Graph (EVG)

    Enforces:
    - Every number belongs to a variable
    - No implicit arithmetic
    - Deterministic factorization
    """

    def __init__(self):
        self.variables: Dict[str, VariableNode] = {}
        self.dependencies: Dict[str, Set[str]] = {}

    # -------------------------------
    # Registration
    # -------------------------------

    def add_variable(
        self,
        name: str,
        value: float | None = None,
        unit: str | None = None,
    ):
        if name not in self.variables:
            self.variables[name] = VariableNode(
                name=name,
                value=value,
                unit=unit,
            )

    def add_dependency(self, parent: str, child: str):
        self.dependencies.setdefault(parent, set()).add(child)

    # -------------------------------
    # Validation
    # -------------------------------

    def unresolved_variables(self) -> List[str]:
        """
        Variables with no assigned value.
        """
        return [
            name
            for name, var in self.variables.items()
            if var.value is None
        ]

    def is_complete(self) -> bool:
        return len(self.unresolved_variables()) == 0

    # -------------------------------
    # Execution
    # -------------------------------

    def compute_product(self, roots: List[str]) -> float:
        """
        Deterministically multiply variables.
        """
        result = 1.0
        visited = set()

        def dfs(node: str):
            nonlocal result
            if node in visited:
                return
            visited.add(node)

            var = self.variables.get(node)
            if not var or var.value is None:
                raise ValueError(
                    f"Unresolved variable used in computation: {node}"
                )

            result *= var.value

            for child in self.dependencies.get(node, []):
                dfs(child)

        for r in roots:
            dfs(r)

        return result
