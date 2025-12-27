from typing import Optional
from .goal_node import GoalNode


class GoalTree:
    def __init__(self, root: GoalNode):
        self.root = root

    def get_next_goal(self) -> Optional[GoalNode]:
        return self._dfs_select(self.root)

    def _dfs_select(self, node: GoalNode) -> Optional[GoalNode]:
        if node.status == "PENDING" and node.is_terminal():
            return node

        for child in sorted(node.children, key=lambda c: -c.priority):
            result = self._dfs_select(child)
            if result:
                return result

        return None

    def mark_goal_satisfied(self, goal: GoalNode):
        goal.mark_satisfied()
        self._propagate(goal.parent)

    def _propagate(self, node: Optional[GoalNode]):
        if not node:
            return

        if all(child.status == "SATISFIED" for child in node.children):
            node.mark_satisfied()
            self._propagate(node.parent)

    def is_complete(self) -> bool:
        return self.root.status == "SATISFIED"
