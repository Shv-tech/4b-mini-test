from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Variable:
    name: str
    role: str
    domain: str = "real"   # int | real | positive
    unit: Optional[str] = None


@dataclass
class Relation:
    expression: str  # symbolic form, e.g. "total = n_people * tickets_per_person"


@dataclass
class LogicalCanonicalForm:
    problem_class: str  # arithmetic | algebra | probability | logic
    givens: List[Variable] = field(default_factory=list)
    unknowns: List[Variable] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    required_output: str = ""

    def all_variables(self) -> Dict[str, Variable]:
        return {v.name: v for v in self.givens + self.unknowns}
