from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PlanStep:
    id: int
    description: str
    constraints: List[str]
    completed: bool = False
    output: Optional[str] = None
