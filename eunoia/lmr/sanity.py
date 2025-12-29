from eunoia.lmr.lcf import LogicalCanonicalForm


class SanityViolation(Exception):
    pass


class SanityEnforcer:
    """
    Refuses ill-posed logical problems.
    """

    def enforce(self, lcf: LogicalCanonicalForm):
        if not lcf.unknowns:
            raise SanityViolation("No unknowns defined.")

        if not lcf.required_output:
            raise SanityViolation("No required output specified.")

        self._domain_checks(lcf)

    def _domain_checks(self, lcf: LogicalCanonicalForm):
        for v in lcf.givens + lcf.unknowns:
            if v.domain not in {"int", "real", "positive"}:
                raise SanityViolation(
                    f"Invalid domain '{v.domain}' for variable '{v.name}'"
                )
