class WorldState:
    def __init__(self):
        self.entities = {}
        self.relationships = {}
        self.time = 0

    def update(self, changes: dict):
        for k, v in changes.items():
            self.entities[k] = v
        self.time += 1

    def snapshot(self):
        return {
            "time": self.time,
            "entities": dict(self.entities),
            "relationships": dict(self.relationships),
        }
