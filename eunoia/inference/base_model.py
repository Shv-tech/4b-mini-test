class BaseModel:
    """
    Abstract base class for all LLM adapters used by Eunoia.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("BaseModel.generate() must be implemented")
