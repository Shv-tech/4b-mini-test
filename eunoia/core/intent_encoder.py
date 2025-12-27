from dataclasses import dataclass
from typing import List
import re


# ----------------------------
# Data container
# ----------------------------

@dataclass
class IntentFrame:
    intent_type: str
    constraints: List[str]
    content: str
    raw_prompt: str


# ----------------------------
# Intent Encoder
# ----------------------------

class IntentEncoder:
    def encode(self, prompt: str) -> IntentFrame:
        # reset raw constraint cache per call
        self._raw_constraint_spans: List[str] = []

        intent = self._detect_intent(prompt)
        constraints = self._extract_constraints(prompt)
        content = self._extract_content(prompt)

        return IntentFrame(
            intent_type=intent,
            constraints=constraints,
            content=content,
            raw_prompt=prompt,
        )

    # ----------------------------
    # Intent Detection
    # ----------------------------

    def _detect_intent(self, prompt: str) -> str:
        p = prompt.lower()

        if re.search(r"\b(step[- ]by[- ]step|steps|procedure|process)\b", p):
            return "PROCEDURE"
        if re.search(r"\b(explain|describe|teach)\b", p):
            return "EXPLANATION"
        if re.search(r"\b(plan|strategy|roadmap)\b", p):
            return "PLANNING"
        if re.search(r"\b(analyze|compare|evaluate)\b", p):
            return "ANALYSIS"

        return "UNKNOWN"

    # ----------------------------
    # Constraint Extraction
    # ----------------------------

    def _extract_constraints(self, prompt: str) -> List[str]:
        constraints: List[str] = []
        p = prompt.lower()

        # exactly N steps / points / sentences
        for m in re.finditer(r"exactly (\d+) (steps|points|sentences)", p):
            constraints.append(f"steps:{m.group(1)}")
            self._raw_constraint_spans.append(m.group(0))

        # no bullets
        for m in re.finditer(r"no (bullets|bullet points)", p):
            constraints.append("format:no_bullets")
            self._raw_constraint_spans.append(m.group(0))

        # tone constraint
        for m in re.finditer(
            r"in (a )?(calm|formal|casual|professional) tone", p
        ):
            constraints.append(f"tone:{m.group(2)}")
            self._raw_constraint_spans.append(m.group(0))

        # length constraint
        for m in re.finditer(r"under (\d+) (words|sentences)", p):
            constraints.append(f"length:<{m.group(1)}")
            self._raw_constraint_spans.append(m.group(0))

        # remove duplicates, preserve order
        return list(dict.fromkeys(constraints))

    # ----------------------------
    # Content Cleaning (FINAL)
    # ----------------------------

    def _extract_content(self, prompt: str) -> str:
        content = prompt

        # 1. Remove raw constraint phrases
        for raw in self._raw_constraint_spans:
            content = re.sub(
                re.escape(raw),
                "",
                content,
                flags=re.IGNORECASE,
            )

        # 2. Remove leading intent verbs ONLY at start
        content = re.sub(
            r"^\s*(write|give|provide|list|create|generate)\b[\s,.:;-]*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        # 3. Normalize punctuation and spacing
        content = re.sub(r"\s*,\s*", ", ", content)
        content = re.sub(r"\s*\.\s*", ". ", content)
        content = re.sub(r"\s{2,}", " ", content)

        return content.strip()
