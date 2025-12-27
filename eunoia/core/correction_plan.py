from dataclasses import dataclass
from typing import List
from eunoia.core.constraint_graph import ConstraintNode


@dataclass
class CorrectionPlan:
    prompt: str
    instructions: List[str]
    violations: List[ConstraintNode]
    should_regenerate: bool = True
