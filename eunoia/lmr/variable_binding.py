import re
from typing import List, Set
from eunoia.lmr.lcf import LogicalCanonicalForm


class VariableBindingError(Exception):
    pass


class VariableBindingEngine:
    """
    Enforces:
    1. Every number belongs to exactly one variable
    2. Every variable appears in at least one relation
    3. No implicit quantities
    """

    NUMBER_PATTERN = re.compile(r"\b\d+(\.\d+)?\b")

    def enforce(self, lcf: LogicalCanonicalForm):
        self._check_numbers_bound(lcf)
        self._check_variables_used(lcf)
        self._check_relations_complete(lcf)

    def _check_numbers_bound(self, lcf: LogicalCanonicalForm):
        text = " ".join(r.expression for r in lcf.relations)
        numbers = set(self.NUMBER_PATTERN.findall(text))

        if numbers:
            raise VariableBindingError(
                f"Found raw numbers in relations: {numbers}. "
                "All quantities must be represented as variables."
            )

    def _check_variables_used(self, lcf: LogicalCanonicalForm):
        used: Set[str] = set()
        for r in lcf.relations:
            for var in lcf.all_variables():
                if var in r.expression:
                    used.add(var)

        unused = set(lcf.all_variables()) - used
        if unused:
            raise VariableBindingError(
                f"Unused variables detected: {unused}"
            )

    def _check_relations_complete(self, lcf: LogicalCanonicalForm):
        if not lcf.relations:
            raise VariableBindingError("No relations defined — cannot solve.")
