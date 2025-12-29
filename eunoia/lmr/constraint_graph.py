from dataclasses import dataclass, field
from typing import Dict, List, Callable


@dataclass
class Constraint:
    name: str
    predicate: Callable[[Dict[str, float]], bool]
    description: str


@dataclass
class ConstraintGraph:
    constraints: List[Constraint] = field(default_factory=list)

    def add(self, constraint: Constraint):
        self.constraints.append(constraint)

    def evaluate(self, values: Dict[str, float]):
        violations = []
        for c in self.constraints:
            if not c.predicate(values):
                violations.append(c.description)
        return violations
