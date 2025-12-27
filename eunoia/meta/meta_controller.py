class MetaController:
    """
    Level 9 — Meta-Controller

    Adjusts reasoning behavior based on performance.
    """

    def __init__(
        self,
        mutation_engine,
        strategy_memory,
        threshold: float = 0.5,
    ):
        self.mutation_engine = mutation_engine
        self.strategy_memory = strategy_memory
        self.threshold = threshold

    def adapt(self, trace, score: float):
        """
        Adapt system-wide behavior based on performance.
        """

        # If reasoning quality is low, encourage exploration
        if score < self.threshold:
            self.mutation_engine.increase_exploration()

        # If reasoning quality is high, favor reuse
        else:
            self.mutation_engine.decrease_exploration()
