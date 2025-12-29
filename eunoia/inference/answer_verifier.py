# eunoia/inference/answer_verifier.py
class AnswerVerifier:
    def verify(self, question: str, proposed: str, solver) -> bool:
        """
        solver: callable(question, mode="verify") -> str
        """
        verify_output = solver(question, mode="verify")
        extracted = FinalAnswerExtractor().extract(verify_output)

        return extracted == proposed
