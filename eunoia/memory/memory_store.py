import json
from pathlib import Path
from typing import List, Dict, Optional

class MemoryStore:
    """
    Persistent, structured memory for Eunoia.
    Stores successful reasoning patterns.
    """

    def __init__(self, path: str = "eunoia_memory.json"):
        self.path = Path(path)
        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def add(self, record: Dict):
        self.memory.append(record)
        self.save()

    def find_similar(self, intent: str, constraints: List[str]) -> Optional[Dict]:
        for record in self.memory:
            if (
                record["intent"] == intent
                and set(record["constraints"]) == set(constraints)
            ):
                return record
        return None
