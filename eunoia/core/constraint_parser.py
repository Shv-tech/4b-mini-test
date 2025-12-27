from eunoia.core.constraint_graph import ConstraintGraph, ConstraintNode


class ConstraintGraphBuilder:
    """
    Converts canonical constraint strings into a ConstraintGraph.
    """

    PRIORITY_MAP = {
        "steps": 100,
        "format": 90,
        "tone": 50,
        "length": 80,
    }

    def build(self, constraints: list[str]) -> ConstraintGraph:
        graph = ConstraintGraph()

        for c in constraints:
            name, value = self._parse_constraint(c)
            priority = self.PRIORITY_MAP.get(name, 10)

            node = ConstraintNode(
                name=name,
                value=value,
                priority=priority,
            )

            graph.add_node(node)

        return graph

    def _parse_constraint(self, constraint: str):
        """
        Example:
        'steps:7' -> ('steps', 7)
        'tone:calm' -> ('tone', 'calm')
        'format:no_bullets' -> ('format', 'no_bullets')
        """
        key, raw_value = constraint.split(":", 1)

        # numeric normalization
        if raw_value.isdigit():
            value = int(raw_value)
        elif raw_value.startswith("<") and raw_value[1:].isdigit():
            value = ("<", int(raw_value[1:]))
        else:
            value = raw_value

        return key, value
