from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController


if __name__ == "__main__":
    model = QwenModel()
    controller = EunoiaController(model, max_iters=3)

    prompt = (
        "Write exactly 3 steps in a calm tone, no bullets. "
        "Explain photosynthesis."
    )

    result = controller.run(prompt)

    print("\n=== FINAL OUTPUT ===")
    print(result["final_output"])

    print("\n=== ITERATION HISTORY ===")
    for h in result["history"]:
        print(h)
