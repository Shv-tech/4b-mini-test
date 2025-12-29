from eunoia.lmr.variable_binding import VariableBindingEngine
from eunoia.lmr.sanity import SanityEnforcer
from eunoia.lmr.lcf import LogicalCanonicalForm


class LMRValidator:
    """
    Absolute gatekeeper before reasoning.
    """

    def __init__(self):
        self.vbe = VariableBindingEngine()
        self.sanity = SanityEnforcer()

    def validate(self, lcf: LogicalCanonicalForm):
        self.sanity.enforce(lcf)
        self.vbe.enforce(lcf)
