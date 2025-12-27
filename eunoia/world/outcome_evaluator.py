from typing import Dict, Any
from eunoia.world.expectation import Expectation


class OutcomeEvaluator:
    """
    Level 8.3 — Compares actual output against expectations.
    """

    def evaluate(
        self,
        output: str,
        expectation: Expectation,
    ) -> Dict[str, Any]:
        failures = []

        # Check mentions
        mentions = expectation.expected_properties.get("mentions", [])
        for term in mentions:
            if term.lower() not in output.lower():
                failures.append(f"Missing expected mention: {term}")

        # Check minimum length
        min_length = expectation.expected_properties.get("min_length")
        if min_length and len(output) < min_length:
            failures.append("Output shorter than expected")

        success = len(failures) == 0

        return {
            "success": success,
            "failures": failures,
            "confidence_penalty": 0.2 * len(failures),
        }
