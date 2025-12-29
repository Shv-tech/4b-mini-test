# eunoia/inference/answer_lock.py
class AnswerLock:
    def __init__(self):
        self.locked = False
        self.answer = None

    def commit(self, answer: str):
        self.locked = True
        self.answer = answer

    def render(self) -> str:
        return f"Answer: {self.answer}"
