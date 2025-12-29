import re
from typing import List, Tuple
from eunoia.core.variable_graph import VariableGraph


NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")


class FactorExtractionError(Exception):
    pass


class FactorExtractor:
    """
    Extracts explicit numeric factors from model output
    and enforces VariableGraph binding.

    Rule:
    ❗ Every number must belong to a variable
    """

    def extract_numbers(self, text: str) -> List[str]:
        return NUMBER_RE.findall(text)

    def bind_factors(
        self,
        text: str,
        graph: VariableGraph,
        variable_order: List[str],
    ):
        numbers = self.extract_numbers(text)

        if len(numbers) > len(variable_order):
            raise FactorExtractionError(
                "More numbers than declared variables"
            )

        for name, value in zip(variable_order, numbers):
            graph.add_variable(name, float(value))

        unresolved = graph.unresolved_variables()
        if unresolved:
            raise FactorExtractionError(
                f"Unresolved variables: {unresolved}"
            )
