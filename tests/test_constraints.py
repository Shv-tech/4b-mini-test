from eunoia.core.constraint_parser import ConstraintGraphBuilder


def test_constraint_graph_builder():
    builder = ConstraintGraphBuilder()

    constraints = [
        "steps:7",
        "tone:calm",
        "format:no_bullets",
    ]

    graph = builder.build(constraints)

    assert len(graph.nodes) == 3

    assert graph.get_node("steps").value == 7
    assert graph.get_node("tone").value == "calm"
    assert graph.get_node("format").value == "no_bullets"

    assert graph.get_node("steps").priority > graph.get_node("tone").priority
