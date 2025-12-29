class LogicalState:
    def __init__(self):
        self.variables = {}
        self.inputs = []
        self.outputs = []
        self.effects = []
        self.causes = []
        self.estimated = None
        self.calculated = None
        self.tolerance = 1e-6
        self.min_allowed = -1e9
        self.max_allowed = 1e9