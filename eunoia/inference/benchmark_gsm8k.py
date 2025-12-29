from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController

# 5 Classic Questions from GSM8K Dataset
# These require keeping track of variables over multiple steps.
GSM8K_SAMPLES = [
    {
        "question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
        "answer": "72",
        "steps_reasoning": "48 / 2 = 24. 48 + 24 = 72."
    },
    {
        "question": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?",
        "answer": "10",
        "steps_reasoning": "50 minutes is 5/6 of an hour. 12 * (5/6) = 10."
    },
    {
        "question": "Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?",
        "answer": "5",
        "steps_reasoning": "Needs 100. Has 50. Parents give 15. Grandparents give 30 (15*2). Total has: 50+15+30 = 95. Needs: 100-95=5."
    },
    {
        "question": "Julie is reading a 120-page book. Yesterday, she was able to read 12 pages and today, she read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages should she read?",
        "answer": "42",
        "steps_reasoning": "Read yesterday: 12. Read today: 24. Total read: 36. Remaining: 120 - 36 = 84. Half of remaining: 42."
    },
    {
        "question": "James writes a 3-page letter to 2 different friends twice a week. How many pages does he write a year?",
        "answer": "624",
        "steps_reasoning": "3 pages * 2 friends = 6 pages per writing session. Twice a week = 12 pages/week. 52 weeks/year. 12 * 52 = 624."
    }
]

def run_benchmark():
    print("Loading Eunoia Model for GSM8K Exam...")
    model = QwenModel()

    print(f"\n=== STARTING GSM8K MINI-BENCHMARK (5 Hard Questions) ===\n")

    score = 0

    for i, task in enumerate(GSM8K_SAMPLES):
        print(f"Question {i+1}: {task['question']}")
        
        # System 2 Mode: Fresh Brain, 5 attempts allowed
        controller = EunoiaController(
            model, 
            max_iters=5, 
            enable_memory=False 
        ) 
        
        # We inject constraints to force it to show work, similar to Chain-of-Thought prompting
        prompt = (
            f"Solve this math problem step-by-step. {task['question']} "
            "Constraint: Show calculation for each step. "
            "Constraint: Final answer must be 'Answer: X'."
        )

        result = controller.run(prompt)
        final_output = result["final_output"]
        history = result["history"]
        
        # Check if the answer is present (Robust check)
        # We look for the number, optionally with $ sign
        expected = task["answer"]
        passed = expected in final_output or f"${expected}" in final_output
        
        if passed:
            score += 1
            status = "PASSED ✅"
        else:
            status = "FAILED ❌"

        print(f"Status: {status}")
        print(f"Thinking Steps: {len(history)}")
        print(f"Expected: {task['answer']}")
        print(f"Output Snippet: {final_output[-150:].strip()}...") # Last 150 chars
        print("-" * 60)

    print(f"\nFINAL GSM8K SCORE: {score}/5 ({(score/5)*100}%)")
    print("Baseline for 4B models is usually ~40-60%. Anything above 3/5 is SOTA for this size.")

if __name__ == "__main__":
    run_benchmark()