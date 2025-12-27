from eunoia.core.intent_encoder import IntentEncoder


def test_intent_and_constraints():
    encoder = IntentEncoder()

    prompt = (
        "Write exactly 7 steps in a calm tone, no bullets. "
        "Explain quantum entanglement."
    )

    frame = encoder.encode(prompt)

    # intent
    assert frame.intent_type == "PROCEDURE"

    # canonical constraints
    assert "steps:7" in frame.constraints
    assert "tone:calm" in frame.constraints
    assert "format:no_bullets" in frame.constraints

    # cleaned content
    assert frame.content == "Explain quantum entanglement."
