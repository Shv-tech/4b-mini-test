from eunoia.core.constraint_parser import ConstraintGraphBuilder
from eunoia.core.constraint_evaluator import ConstraintEvaluator


def test_constraint_evaluation_pass():
    builder = ConstraintGraphBuilder()
    evaluator = ConstraintEvaluator()

    graph = builder.build([
        "steps:2",
        "format:no_bullets",
    ])

    output = "1. First step\n2. Second step"

    result = evaluator.evaluate(graph, output)

    assert result["is_compliant"] is True
    assert result["violations"] == []


def test_constraint_evaluation_fail():
    builder = ConstraintGraphBuilder()
    evaluator = ConstraintEvaluator()

    graph = builder.build([
        "steps:2",
        "format:no_bullets",
    ])

    output = "- Step one\n- Step two"

    result = evaluator.evaluate(graph, output)

    assert result["is_compliant"] is False
    assert len(result["violations"]) == 2
