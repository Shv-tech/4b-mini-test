# eunoia/inference/final_answer.py
import re
from typing import Optional

class FinalAnswerExtractor:
    NUMBER_PATTERN = re.compile(r"-?\d+(\.\d+)?")

    def extract(self, text: str) -> Optional[str]:
        # Priority patterns
        patterns = [
            r"answer\s*[:=]\s*(-?\d+(\.\d+)?)",
            r"therefore\s*(-?\d+(\.\d+)?)",
            r"so\s*(-?\d+(\.\d+)?)",
        ]

        text_lower = text.lower()

        for p in patterns:
            match = re.search(p, text_lower)
            if match:
                return match.group(1)

        # Fallback: last number in text
        numbers = self.NUMBER_PATTERN.findall(text)
        if numbers:
            return numbers[-1][0]

        return None
