from typing import List, Optional


class GoalNode:
    def __init__(
        self,
        goal_id: int,
        description: str,
        priority: float = 1.0,
        parent: Optional["GoalNode"] = None,
    ):
        self.goal_id = goal_id
        self.description = description
        self.priority = priority
        self.parent = parent
        self.children: List["GoalNode"] = []
        self.status = "PENDING"  # PENDING | SATISFIED | ABANDONED

    def add_child(self, child: "GoalNode"):
        child.parent = self
        self.children.append(child)

    def mark_satisfied(self):
        self.status = "SATISFIED"

    def abandon(self):
        self.status = "ABANDONED"

    def is_terminal(self) -> bool:
        return len(self.children) == 0

    def __repr__(self):
        return f"<Goal {self.goal_id} | {self.status} | p={self.priority}>"
