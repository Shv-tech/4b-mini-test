from eunoia.world.world_state import WorldState
from eunoia.world.counterfactual import CounterfactualEngine
from eunoia.world.temporal import TemporalConsistencyChecker
from eunoia.world.invariants.conservation import ConservationInvariant
from eunoia.world.invariants.structure import StructuralIntegrityInvariant


class WorldModelOmega:
    def __init__(self):
        self.state = WorldState()
        self.counterfactual = CounterfactualEngine()
        self.temporal = TemporalConsistencyChecker()
        self.invariants = [
            ConservationInvariant(),
            StructuralIntegrityInvariant(),
        ]

    def apply(self, action: dict):
        before = self.state.snapshot()
        self.state.update(action)

        for inv in self.invariants:
            inv.check(self.state)

        self.temporal.verify(before, self.state)

    def simulate_and_check(self, action):
        future = self.counterfactual.simulate(self.state, action)
        for inv in self.invariants:
            inv.check(future)
        return True