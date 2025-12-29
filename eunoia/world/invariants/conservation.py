from eunoia.world.invariants.base import Invariant


class ConservationInvariant(Invariant):
    name = "conservation"

    def check(self, world):
        total = sum(world.entities.values())
        if abs(total) > 1e12:
            raise ValueError("Conservation law violated")