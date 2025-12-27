from eunoia.world.world_consistency import WorldConsistencyMemory


def test_world_consistency_blocks_contradiction():
    memory = WorldConsistencyMemory()

    memory.record(["Photosynthesis occurs in chloroplasts"])

    assert memory.check(["Photosynthesis occurs in chloroplasts"])
    assert not memory.check(["not photosynthesis occurs in chloroplasts"])
