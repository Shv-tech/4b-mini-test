from typing import Dict, Any


class BeliefState:
    """
    Level 8.1 — Belief State
    Backward-compatible with existing tests.
    """

    def __init__(self):
        self._beliefs: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._beliefs[key] = value

    def get(self, key: str, default=None):
        return self._beliefs.get(key, default)

    def update(self, new_beliefs: Dict[str, Any]):
        self._beliefs.update(new_beliefs)

    def revise(self, key: str, new_value: Any):
        self._beliefs[key] = new_value

    def remove(self, key: str):
        if key in self._beliefs:
            del self._beliefs[key]

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._beliefs)

    def __repr__(self):
        return f"BeliefState({self._beliefs})"
