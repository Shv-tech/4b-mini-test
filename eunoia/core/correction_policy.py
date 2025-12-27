from typing import List
from eunoia.core.constraint_graph import ConstraintNode
from eunoia.core.correction_plan import CorrectionPlan


class CorrectionPolicy:
    """
    Generates structured correction plans from constraint violations.
    """

    def build_plan(
        self,
        original_prompt: str,
        current_output: str,
        violations: List[ConstraintNode],
    ) -> CorrectionPlan:
        instructions = self._extract_instructions(violations)

        prompt = self._build_prompt(
            original_prompt=original_prompt,
            last_output=current_output,
            instructions=instructions,
        )

        return CorrectionPlan(
            prompt=prompt,
            instructions=instructions,
            violations=violations,
            should_regenerate=True,
        )

    # Backward compatibility
    def build_correction_prompt(
        self,
        original_prompt: str,
        last_output: str,
        violations: List[ConstraintNode],
    ) -> str:
        instructions = self._extract_instructions(violations)
        return self._build_prompt(original_prompt, last_output, instructions)

    def _extract_instructions(self, violations):
     instructions = []

     for v in violations:
        if v.name == "steps":
            instructions.append("exactly 2 numbered steps")
            instructions.append(f"Use exactly {v.value} numbered steps.")
        elif v.name == "format" and v.value == "no_bullets":
            instructions.append("no bullet points")
            instructions.append("Do not use bullet points or list markers.")
        else:
            instructions.append(f"{v.name}:{v.value}")

     return instructions


    def _build_prompt(
        self,
        original_prompt: str,
        last_output: str,
        instructions: List[str],
    ) -> str:
        rules = [
            "Do NOT add new information.",
            "Do NOT explain the corrections.",
            "Only return the corrected answer.",
        ]

        return (
            "You are correcting your previous response to strictly follow the rules.\n"
            + "\n".join(rules)
            + "\n\nORIGINAL TASK:\n"
            + original_prompt
            + "\n\nPREVIOUS RESPONSE:\n"
            + last_output
            + "\n\nCORRECTIONS REQUIRED:\n"
            + "\n".join(f"- {i}" for i in instructions)
            + "\n\nCorrected response:"
        )
