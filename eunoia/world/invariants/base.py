class Invariant:
    name: str

    def check(self, world_state: "WorldState"):
        raise NotImplementedError