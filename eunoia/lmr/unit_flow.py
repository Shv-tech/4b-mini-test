class UnitFlowError(Exception):
    pass


class UnitFlowGraph:
    """
    Enforces valid unit transformations.
    """

    def __init__(self):
        self.edges = []

    def add_flow(self, src_unit: str, dst_unit: str):
        self.edges.append((src_unit, dst_unit))

    def validate(self, start: str, end: str):
        visited = set()
        stack = [start]

        while stack:
            u = stack.pop()
            if u == end:
                return True
            for a, b in self.edges:
                if a == u and b not in visited:
                    visited.add(b)
                    stack.append(b)

        raise UnitFlowError(f"Invalid unit flow: {start} → {end}")
