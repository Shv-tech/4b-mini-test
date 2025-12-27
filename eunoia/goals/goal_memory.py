from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import time
import re
from difflib import SequenceMatcher

# Expanded stopword list to focus on content words
STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "for", "with", "on", "at", 
    "by", "from", "up", "about", "into", "over", "after"
}

def generate_semantic_signature(text: str) -> str:
    """
    Creates a robust, order-independent signature of the goal.
    
    Input:  "Build a Python Web Server"
    Output: "build_python_server_web"
    
    Input:  "Server for web made in python"
    Output: "build_python_server_web" (matches above)
    """
    # 1. Lowercase and clean
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    
    # 2. Tokenize and filter stopwords
    tokens = [t for t in text.split() if t not in STOPWORDS]
    
    # 3. Sort tokens to make signature independent of word order
    tokens.sort()
    
    # 4. Join. If empty (rare), fallback to original cropped.
    if not tokens:
        return text.strip()[:20]
        
    return "_".join(tokens)


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
            # Update children if the new path is different? 
            # For now, we keep the first success or you could merge them.
        else:
            self.memory[sig] = GoalMemoryEntry(
                goal_signature=sig,
                original_text=parent_goal,
                successful_children=children,
            )

    def recall(self, goal_text: str, similarity_threshold: float = 0.85) -> Optional[List[str]]:
        """
        Recalls strategy with fuzzy fallback.
        """
        sig = generate_semantic_signature(goal_text)
        
        # 1. Exact Semantic Match (Fast)
        if sig in self.memory:
            entry = self.memory[sig]
            entry.last_used = time.time()
            return entry.successful_children
            
        # 2. Fuzzy Match (Slower, but catches "Build http server" vs "Build web server")
        # Only runs if exact match fails.
        best_ratio = 0.0
        best_entry = None
        
        for entry in self.memory.values():
            # Compare signatures, not raw text, for better semantic overlap
            ratio = SequenceMatcher(None, sig, entry.goal_signature).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_entry = entry
                
        if best_entry and best_ratio >= similarity_threshold:
            best_entry.last_used = time.time()
            return best_entry.successful_children

        return None