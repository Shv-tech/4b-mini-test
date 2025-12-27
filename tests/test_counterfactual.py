from eunoia.world.counterfactual import CounterfactualSimulator


def test_counterfactual_simulation_generates_alternatives():
    simulator = CounterfactualSimulator()

    alts = simulator.simulate("Explain photosynthesis")

    assert len(alts) >= 3
    assert any("define photosynthesis" in a.lower() for a in alts)
