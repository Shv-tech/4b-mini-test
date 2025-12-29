class StructuralIntegrityInvariant(Invariant):
    name = "structural_integrity"

    def check(self, world):
        for e, v in world.entities.items():
            if v is None:
                raise ValueError(f"Broken structure at {e}")