from eunoia.core.constraint_parser import ConstraintGraphBuilder
from eunoia.core.constraint_evaluator import ConstraintEvaluator
from eunoia.core.correction_policy import CorrectionPolicy


def test_correction_policy_generates_plan():
    builder = ConstraintGraphBuilder()
    evaluator = ConstraintEvaluator()
    policy = CorrectionPolicy()

    graph = builder.build([
        "steps:2",
        "format:no_bullets",
    ])

    bad_output = "- Step one\n- Step two"

    eval_result = evaluator.evaluate(graph, bad_output)
    violations = eval_result["violations"]

    plan = policy.build_plan(
        original_prompt="Explain X",
        current_output=bad_output,
        violations=violations,
    )

    assert plan.should_regenerate is True
    assert "exactly 2 numbered steps" in plan.instructions
    
    # FIXED: Updated assertion to match the actual implementation in correction_policy.py
    assert "Do not use bullet points or list markers." in plan.instructions
    
    # You could also check for the short form if preferred:
    # assert "no bullet points" in plan.instructions
    
    # Check that constraint names are in the violation list
    violation_names = [v.name for v in plan.violations]
    assert "steps" in violation_names
    assert "format" in violation_names