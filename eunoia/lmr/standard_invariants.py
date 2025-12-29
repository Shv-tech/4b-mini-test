from eunoia.lmr.invariants import Invariant


def non_negative(var: str):
    return Invariant(
        name=f"{var} >= 0",
        check=lambda v: v[var] >= 0
    )


def integer(var: str):
    return Invariant(
        name=f"{var} is integer",
        check=lambda v: float(v[var]).is_integer()
    )


def conservation(lhs: str, rhs_vars: list[str]):
    """
    lhs = sum(rhs_vars)
    """
    return Invariant(
        name=f"Conservation: {lhs}",
        check=lambda v: abs(v[lhs] - sum(v[x] for x in rhs_vars)) < 1e-6
    )
