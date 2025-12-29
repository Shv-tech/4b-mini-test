class TemporalConsistencyChecker:
    def verify(self, previous, current):
        if current.time <= previous.time:
            raise ValueError("Time regression detected")