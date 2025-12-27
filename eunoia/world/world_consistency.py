from typing import List, Set, Tuple

class WorldConsistencyMemory:
    """
    Level 8.5 — World Consistency Memory (Enhanced)
    
    Uses a Polarity-Based Logic check rather than raw string matching.
    Input: "The sky is blue" -> stores ("the sky is blue", Positive)
    Check: "The sky is not blue" -> parses ("the sky is blue", Negative) -> CONTRADICTION
    """

    def __init__(self):
        # Stores normalized statement -> polarity (True=Positive, False=Negative)
        self._knowledge_base: Set[Tuple[str, bool]] = set()

    def _normalize_and_detect_polarity(self, text: str) -> Tuple[str, bool]:
        """
        Separates the core proposition from its truth value.
        
        "The sky is not blue" -> ("the sky is blue", False)
        "The user is 19 years old" -> ("the user is 19 years old", True)
        """
        text = text.strip().lower()
        
        # 1. Explicit Negation Markers
        negations = [
            " is not ", " are not ", " does not ", " do not ", 
            " cannot ", " can't ", " won't ", " will not ",
            " never ", " isn't ", " aren't ", " doesn't "
        ]
        
        for neg in negations:
            if neg in text:
                # Remove the negation marker to get the positive proposition
                # e.g. "sky is not blue" -> "sky blue" (simplified for matching)
                # Better: Replace with space to preserve boundaries
                clean_prop = text.replace(neg, " ")
                # Collapse spaces
                clean_prop = " ".join(clean_prop.split())
                return clean_prop, False

        # 2. Prefix Negation
        if text.startswith("not "):
            return text[4:].strip(), False
            
        # 3. Explicit "False" statement (e.g., "It is false that X")
        if "it is false that " in text:
             return text.replace("it is false that ", "").strip(), False

        # Default: Positive
        return text, True

    def record(self, facts: List[str]):
        """
        Ingests new facts into the consistency DB.
        """
        for f in facts:
            proposition, polarity = self._normalize_and_detect_polarity(f)
            self._knowledge_base.add((proposition, polarity))

    def check(self, new_facts: List[str]) -> bool:
        """
        Returns True if facts are consistent.
        Returns False if a contradiction is found.
        """
        for f in new_facts:
            prop, new_polarity = self._normalize_and_detect_polarity(f)
            
            # Check against KB
            # If we have the SAME proposition but OPPOSITE polarity -> Contradiction
            
            # Case 1: Direct Contradiction
            # KB: ("sky blue", True) vs New: ("sky blue", False)
            if (prop, not new_polarity) in self._knowledge_base:
                return False

        return True

    def snapshot(self) -> List[str]:
        # Reconstruct readable strings for debugging
        output = []
        for prop, polarity in self._knowledge_base:
            prefix = "" if polarity else "NOT "
            output.append(f"{prefix}({prop})")
        return output

    def get_contradiction_reason(self, new_fact: str) -> str:
        """
        Helper to explain WHY it failed (useful for debugging/logs).
        """
        prop, new_pol = self._normalize_and_detect_polarity(new_fact)
        if (prop, not new_pol) in self._knowledge_base:
            return f"Contradiction: You previously believed '{prop}' was {not new_pol}, now claiming it is {new_pol}."
        return ""