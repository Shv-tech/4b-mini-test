from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController

# --- THE "BEAST MODE" DATASET ---
WORLD_TOUR_TASKS = [
    # --- CATEGORY 1: IMPOSSIBLE LOGIC (LHR) ---
    {
        "name": "The Zebra Logic Grid",
        "prompt": (
            "Solve this logic puzzle. "
            "1. There are 5 houses in a row. "
            "2. The Red house is to the left of the Green. "
            "3. The German lives in the Red house. "
            "4. The Brit owns a dog. "
            "5. The owner of the Green house drinks coffee. "
            "6. The owner of the Yellow house smokes Dunhill. "
            "7. The man in the center house drinks milk. "
            "8. The Norwegian lives in the first house. "
            "9. The Norwegian lives next to the Blue house. "
            "Question: Who keeps the Fish? "
            "Constraint: Output a JSON object mapping House Number to {Color, Nationality, Pet, Drink, Smoke}."
        ),
        "expected": ["German", "Fish"] 
    },
    {
        "name": "The Liar's Chain",
        "prompt": (
            "Alice says 'Bob is lying'. "
            "Bob says 'Charlie is telling the truth'. "
            "Charlie says 'Alice and Bob are both liars'. "
            "Question: Who is telling the truth? "
            "Constraint: Show the truth table for all possibilities. "
            "Constraint: Final Answer must be one name."
        ),
        "expected": ["Alice"] # Alice=T -> Bob=F (Lying) -> Charlie=F (Lying about A&B being liars? No, if C is lying, then A&B are NOT both liars. A is T, B is F. Correct.)
    },

    # --- CATEGORY 2: DEEP MATH (Tool Use) ---
    {
        "name": "Recursive Interest",
        "prompt": (
            "I invest $1,000. Every month, the value grows by 5%, but every 3rd month, I withdraw $200 (after the growth). "
            "Question: What is the exact value of my account after 24 months? "
            "Constraint: Write a Python script to simulate this month-by-month. "
            "Constraint: Print the final value."
        ),
        "expected": ["632", "633"] # Approx range depending on float handling
    },
    {
        "name": "Unit Conversion Hell",
        "prompt": (
            "A snail travels 500 furlongs per fortnight. "
            "Question: What is its speed in centimeters per second? "
            "Constraint: Show the explicit chain of conversion factors. "
            "Constraint: 1 furlong = 201.168 meters. 1 fortnight = 14 days."
        ),
        "expected": ["0.83", "0.8"] # ~0.83 cm/s
    },

    # --- CATEGORY 3: REALITY CHECK (World Model) ---
    {
        "name": "The Thermodynamic Demon",
        "prompt": (
            "Design a machine that takes 100J of heat from a cold reservoir at 200K and transfers it to a hot reservoir at 300K without any external work input. "
            "Question: Calculate the Coefficient of Performance. "
        ),
        "expected": ["violate", "law of thermodynamics", "impossible", "entropy"]
    },
    {
        "name": "Infinite Acceleration",
        "prompt": (
            "A spaceship of mass 1000kg accelerates from 0 to 300,000,000 m/s in 10 seconds. "
            "Question: Calculate the force required using F=ma. "
        ),
        "expected": ["relativity", "speed of light", "impossible", "c is", "violation"]
    },

    # --- CATEGORY 4: CONSTRAINT JACKET (Formatting) ---
    {
        "name": "The Oulipo Challenge",
        "prompt": (
            "Summarize the plot of the movie 'Titanic' in exactly 50 words. "
            "Constraint 1: Do not use the letter 'e'. "
            "Constraint 2: The summary must be a single paragraph. "
            "Constraint 3: The last word must be 'sank'."
        ),
        "expected": ["sank"] # Visual check needed for 'e'
    },
    {
        "name": "The Rhyming Coder",
        "prompt": (
            "Write a Python function to calculate the Fibonacci sequence. "
            "Constraint: Every comment in the code must be a rhyming couplet explaining the line below it."
        ),
        "expected": ["def fib", "return"] # Visual check needed for rhymes
    },

    # --- CATEGORY 5: META-COGNITION ---
    {
        "name": "The Self-Audit",
        "prompt": (
            "Solve: 'If a rooster lays an egg on the roof, which way does it roll?' "
            "Constraint: Before answering, output your ReasoningTraceSchema JSON showing entities and constraints."
        ),
        "expected": ["rooster", "lay", "egg", "impossible", "cannot"]
    },
    {
        "name": "Context Switch Speedrun",
        "prompt": (
            "Step 1: Solve 25 * 48. "
            "Step 2: Translate the result into Roman Numerals. "
            "Step 3: Write a Haiku where the number of syllables in the first line equals that Roman Numeral's character count. "
            "Constraint: Perfect execution of all 3 chained steps."
        ),
        "expected": ["1200", "MCC", "3"] # MCC is 3 chars. Haiku line 1 needs 3 syllables.
    }
]

def run_benchmark():
    print("Loading Eunoia-4b-mini...")
    print("Preparing to run Benchmark test 3 (10 Tasks)...")
    model = QwenModel()

    score = 0

    for i, task in enumerate(WORLD_TOUR_TASKS):
        print(f"\nTask {i+1}: {task['name']}")
        print("-" * 60)
        
        # OMEGA Controller: Memory OFF to prove reasoning, High Confidence Threshold
        controller = EunoiaController(
            model, 
            max_iters=5, 
            enable_memory=False, 
            confidence_threshold=0.75 
        )
        
        result = controller.run(task["prompt"])
        final_output = result["final_output"]
        confidence = result.get("confidence", 0.0)
        logic_verified = result["history"][-1].get("logically_verified", False) if result["history"] else False

        # Soft Grading Logic
        passed_keywords = any(k.lower() in final_output.lower() for k in task["expected"])
        
        # Grading
        status = "FAILED ❌"
        if passed_keywords:
            status = "PASSED ✅"
            score += 1
        
        # Exception for Oulipo (Manual Check usually needed, but we check 'sank')
        if task["name"] == "The Oulipo Challenge" and "e" in final_output.replace("The Oulipo Challenge", ""):
             status = "FAILED ❌ (Contains 'e')"
             if passed_keywords: score -= 1 # Revoke point

        print(f"Status: {status}")
        print(f"Logic Verified: {logic_verified} | Confidence: {confidence:.2f}")
        print(f"Output Snippet:\n{final_output.strip()[:300]}...") # First 300 chars
        print("=" * 60)

    print(f"\nFINAL WORLD TOUR SCORE: {score}/10")
    print("Note: Score is heuristic based on keywords. Inspect 'Oulipo' and 'Rhyme' manually.")

if __name__ == "__main__":
    run_benchmark()