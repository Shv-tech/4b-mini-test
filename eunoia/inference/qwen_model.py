# eunoia/inference/qwen_model.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from eunoia.inference.base_model import BaseModel

class QwenModel(BaseModel):
    def __init__(self):
        model_id = "Qwen/Qwen3-4B-Instruct-2507"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )

        self.model.eval()

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
                temperature=0.2,
                pad_token_id=self.tokenizer.eos_token_id
            )

        return self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True
        )
