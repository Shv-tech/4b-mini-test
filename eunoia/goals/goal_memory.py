from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import re
from difflib import SequenceMatcher

STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "for", "with", "on", "at",
    "by", "from", "up", "about", "into", "over", "after"
}


def generate_semantic_signature(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    tokens = [t for t in text.split() if t not in STOPWORDS]
    tokens.sort()
    return "_".join(tokens) if tokens else text[:20]


@dataclass
class GoalMemoryEntry:
    goal_signature: str
    original_text: str
    successful_children: List[str]
    success_count: int = 1
    last_used: float = field(default_factory=time.time)


class GoalMemory:
    def __init__(self):
        self.memory: Dict[str, GoalMemoryEntry] = {}

    def record_success(self, parent_goal: str, children: List[str]):
        sig = generate_semantic_signature(parent_goal)

        if sig in self.memory:
            entry = self.memory[sig]
            entry.success_count += 1
            entry.last_used = time.time()
        else:
            self.memory[sig] = GoalMemoryEntry(
                goal_signature=sig,
                original_text=parent_goal,
                successful_children=children,
            )

    def recall(self, goal_text: str, similarity_threshold: float = 0.85) -> Optional[List[str]]:
        sig = generate_semantic_signature(goal_text)

        if sig in self.memory:
            self.memory[sig].last_used = time.time()
            return self.memory[sig].successful_children

        best_ratio = 0.0
        best_entry = None

        for entry in self.memory.values():
            ratio = SequenceMatcher(None, sig, entry.goal_signature).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_entry = entry

        if best_entry and best_ratio >= similarity_threshold:
            best_entry.last_used = time.time()
            return best_entry.successful_children

        return None
