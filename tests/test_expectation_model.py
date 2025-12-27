from eunoia.world.expectation import ExpectationModel


def test_expectation_registration():
    model = ExpectationModel()

    model.register(
        goal_id=1,
        expected_properties={
            "mentions": ["sunlight", "chloroplast"],
            "min_length": 40,
        },
        confidence=0.9,
    )

    exp = model.get(1)
    assert exp is not None
    assert "sunlight" in exp.expected_properties["mentions"]
    assert exp.confidence == 0.9
