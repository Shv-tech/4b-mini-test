from eunoia.world.outcome_evaluator import OutcomeEvaluator
from eunoia.world.expectation import Expectation


def test_outcome_evaluation_detects_missing_expectation():
    evaluator = OutcomeEvaluator()

    exp = Expectation(
        goal_id=1,
        expected_properties={
            "mentions": ["sunlight", "chloroplast"],
            "min_length": 30,
        },
    )

    output = "Photosynthesis happens in plants."

    result = evaluator.evaluate(output, exp)

    assert result["success"] is False
    assert len(result["failures"]) >= 1
