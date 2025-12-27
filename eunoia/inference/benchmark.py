from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController
from eunoia.core.intent_encoder import IntentEncoder
from eunoia.core.constraint_parser import ConstraintGraphBuilder
from eunoia.core.constraint_evaluator import ConstraintEvaluator


PROMPTS = [
    "Write exactly 3 steps in a calm tone, no bullets. Explain gravity.",
    "Summarize photosynthesis in exactly 2 sentences, no bullet points.",
    "Explain black holes in a calm tone, under 80 words.",
]


def run_baseline(model, prompt):
    return model.generate(prompt)


def run_eunoia(controller, prompt):
    result = controller.run(prompt)
    return result["final_output"], result["history"]


if __name__ == "__main__":
    model = QwenModel()
    controller = EunoiaController(model, max_iters=3)

    intent = IntentEncoder()
    graph_builder = ConstraintGraphBuilder()
    evaluator = ConstraintEvaluator()

    print("\n=== BENCHMARK RESULTS ===\n")

    for p in PROMPTS:
        frame = intent.encode(p)
        graph = graph_builder.build(frame.constraints)

        baseline_out = run_baseline(model, frame.content)
        baseline_eval = evaluator.evaluate(graph, baseline_out)

        eunoia_out, history = run_eunoia(controller, p)
        eunoia_eval = evaluator.evaluate(graph, eunoia_out)

        print("PROMPT:", p)
        print("Baseline compliant:", baseline_eval["is_compliant"])
        print("Eunoia compliant:", eunoia_eval["is_compliant"])
        print("Eunoia iterations:", len(history))
        print("-" * 50)
