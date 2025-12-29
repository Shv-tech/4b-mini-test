from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController

# --- LHR DATASET ---
LHR_TASKS = [
    {
        "name": "Logic Puzzle",
        "prompt": (
            "Solve this logic puzzle step-by-step. "
            "1. Alice, Bob, and Charlie live in Red, Blue, and Green houses. "
            "2. Alice does not live in the Red house. "
            "3. The Green house is immediately to the right of the Red house. "
            "4. Bob lives in the Blue house. "
            "Question: Who lives in which house? "
            "Constraint: Provide the answer as a numbered list of exactly 3 pairings."
        ),
        "expected_keywords": ["Alice", "Green", "Bob", "Blue", "Charlie", "Red"]
    },
    {
        "name": "Constraint Planning",
        "prompt": (
            "Create a workout plan for 3 days (Mon, Wed, Fri). "
            "Constraints: "
            "1. Monday must be Cardio. "
            "2. Wednesday must be Legs, but no squats allowed. "
            "3. Friday must be Upper Body. "
            "4. Total workout time for the week must not exceed 90 mins. "
            "5. Output must be exactly 3 paragraphs."
        ),
        "expected_keywords": ["Monday", "Wednesday", "Friday", "Cardio", "Legs", "Upper Body"]
    },
    {
        "name": "Multi-Step Math",
        "prompt": (
            "Solve this: A store sells apples for $2 and oranges for $3. "
            "Alice buys 4 apples and 5 oranges. She pays with a $50 bill. "
            "How much change does she get? "
            "Constraint: Show your work in exactly 4 steps. "
            "Constraint: Final answer must be 'Change: $X'."
        ),
        "expected_keywords": ["23", "$27", "Change: $27"]
    }
]

def run_benchmark():
    # 1. Initialize the Brain
    print("Loading Eunoia Model...")
    model = QwenModel()

    print(f"\n=== STARTING Long Horizon Reasoning BENCHMARK ({len(LHR_TASKS)} Tasks) ===\n")

    score = 0

    for task in LHR_TASKS:
        print(f"Task: {task['name']}")
        print("-" * 40)
        
        # 🔥 FIX: Re-initialize the Controller here!
        # This gives it a "Fresh Brain" for every single task.
        controller = EunoiaController(model, max_iters=5, enable_memory=False) 
        
        # Run Eunoia Loop
        result = controller.run(task["prompt"])
        final_output = result["final_output"]
        history = result["history"]
        
        # Simple Keyword Evaluation
        passed = all(k.lower() in final_output.lower() for k in task["expected_keywords"])
        
        if passed:
            score += 1
            status = "PASSED ✅"
        else:
            status = "FAILED ❌"

        print(f"Status: {status}")
        print(f"Thinking Steps (Corrections): {len(history)}")
        print(f"Final Output:\n{final_output.strip()}\n")
        print("=" * 60)

    print(f"\nFinal Score: {score}/{len(LHR_TASKS)}")

if __name__ == "__main__":
    run_benchmark()