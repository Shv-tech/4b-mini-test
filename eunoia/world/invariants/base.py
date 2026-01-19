from eunoia.world.world_state import WorldState

class Invariant:
    name: str

    def check(self, world_state: "WorldState"):
        raise NotImplementedError