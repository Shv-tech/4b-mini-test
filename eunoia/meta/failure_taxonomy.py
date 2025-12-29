class FailureTaxonomy:
    TYPES = {
        "logic": "Logical inconsistency",
        "unit": "Unit mismatch",
        "domain": "Wrong domain reasoning",
        "heuristic": "Missing heuristic",
        "world": "Invariant violation",
        "overgeneralization": "Extrapolated beyond support"
    }

    def classify(self, error):
        for key in self.TYPES:
            if key in error.lower():
                return key
        return "unknown"