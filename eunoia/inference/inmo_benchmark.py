import requests
import json
import time
import sys
import logging
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "http://localhost:8000/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# Configure Standard Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("INMO_BENCHMARK")

# --- THE INMO 2026 QUESTION BANK ---
questions = [
    {
        "id": "Q1",
        "title": "The Sequence Squares (Algebra)",
        "prompt": r"""
Let $x_1, x_2, \dots$ be a sequence of positive integers defined as follows: $x_1=1$ and for each $n \ge 1$ we have $x_{n+1} = x_n + \lfloor \sqrt{x_n} \rfloor$.
Determine all positive integers $m$ for which $x_n = m^2$ for some $n \ge 1$.
Constraint: Provide a rigorous step-by-step derivation.
"""
    },
    {
        "id": "Q2",
        "title": "The Frequency Function (Combinatorics)",
        "prompt": r"""
Let $f: \mathbb{N} \to \mathbb{N}$ be a function satisfying the following condition: for each $k > 2026$, the number $f(k)$ equals the maximum number of times a number appears in the list $f(1), f(2), \dots, f(k-1)$.
Prove that for infinitely many $n \in \mathbb{N}$, $f(n) = f(n + f(n))$.
Constraint: Use clear logical steps for the proof.
"""
    },
    {
        "id": "Q3",
        "title": "The 90-Degree Angle (Geometry)",
        "prompt": r"""
Let ABC be an acute-angled scalene triangle with circumcircle $\Gamma$. Let M be the midpoint of BC and N be the midpoint of the minor arc BC of $\Gamma$.
Points P and Q lie on segments AB and AC respectively such that $BP=BN$ and $CQ=CN$. Point $K \ne N$ lies on line AN with $MK=MN$.
Prove that $\angle PKQ = 90^\circ$.
Constraint: Use geometric properties and theorems.
"""
    },
    {
        "id": "Q4",
        "title": "Companions (Number Theory)",
        "prompt": r"""
Two integers a and b are called companions if every prime number p either divides both or none of a, b.
Determine all functions $f: \mathbb{N}_0 \to \mathbb{N}_0$ such that $f(0)=0$ and the numbers $f(m)+n$ and $f(n)+m$ are companions for all $m, n \in \mathbb{N}_0$.
Constraint: Derive the function form step-by-step.
"""
    },
    {
        "id": "Q5",
        "title": "Reflections & Orthocenter (Geometry)",
        "prompt": r"""
Three lines $l_1, l_2, l_3$ form an acute angled triangle T in the plane. Point P lies in the interior of T.
Let $\tau_i$ denote the reflection of any point X in line $l_i$. Denote by $P_{ijk}$ the point $\tau_k(\tau_j(\tau_i(P)))$ for each permutation (i, j, k) of (1, 2, 3).
Prove that the 6 points $P_{123}, P_{132}, P_{213}, P_{231}, P_{312}, P_{321}$ are concyclic if and only if P coincides with the orthocenter of T.
Constraint: Provide a rigorous step-by-step derivation.
"""
    },
    {
        "id": "Q6",
        "title": "The Card Duel (Game Theory)",
        "prompt": r"""
Two decks A and B of 40 cards each are placed on a table. Every minute, we pick top cards $a \in A$ and $b \in B$ to duel.
Outcomes:
1. Winner: placed back at top, Loser: placed at bottom.
2. Evenly matched: both removed.
3. No interaction: both placed at bottom.
The process ends when both decks are empty. Prove that the maximum time a game can last equals 356 hours.
Constraint: Verify the calculation explicitly.
"""
    }
]

def run_benchmark():
    logger.info("INITIATING INMO 2026 BENCHMARK SUITE [MODEL: Eunoia-4B-Mini]")
    logger.info(f"Target Endpoint: {API_URL}")
    print("="*80)

    results_summary = []

    for q in questions:
        logger.info(f"Executing Test Case: {q['id']} - {q['title']}")
        
        payload = {
            "prompt": q['prompt'],
            "max_iters": 12,
            "confidence_threshold": 0.75
        }

        try:
            start_time = time.time()
            response = requests.post(API_URL, json=payload, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            duration = time.time() - start_time

            # Extract Payload
            answer = data.get("answer", "No Answer Returned")
            confidence = data.get("confidence", 0.0)
            steps = data.get("steps", 0)
            thinking_trace = data.get("thinking_trace", [])

            # --- LOGGING THE TRACE ---
            print("\n" + "-"*30 + f" THINKING TRACE: {q['id']} " + "-"*30)
            if thinking_trace:
                for step in thinking_trace:
                    iteration = step.get('iteration', 'N/A')
                    role = step.get('role', 'unknown')
                    
                    if role == 'tool_execution':
                        tool_out = step.get('tool_output', '')
                        # Truncate long outputs for readability
                        if len(tool_out) > 300:
                            tool_out = tool_out[:300] + "... [TRUNCATED]"
                        print(f"[ITERATION {iteration}] [TOOL EXECUTION] Output: {tool_out}")
                    else:
                        verified_flag = "VERIFIED" if step.get('logically_verified') else "UNVERIFIED"
                        conf_score = step.get('confidence', 0.0)
                        print(f"[ITERATION {iteration}] [REASONING] Status: {verified_flag} | Confidence: {conf_score:.4f}")
            else:
                print("[WARNING] No thinking trace returned from server.")
            print("-" * 80)

            # --- LOGGING THE ANSWER ---
            logger.info(f"Test Case {q['id']} Completed in {duration:.2f}s | Iterations: {steps} | Confidence: {confidence:.4f}")
            print("\n" + "*"*30 + " FINAL MODEL OUTPUT " + "*"*30)
            print(answer)
            print("*" * 80 + "\n")
            
            # Store Metrics
            results_summary.append({
                "id": q['id'],
                "status": "PASS" if confidence > 0.7 else "LOW_CONFIDENCE",
                "iterations": steps,
                "latency": duration
            })

        except requests.exceptions.ConnectionError:
            logger.critical(f"Connection Failed for {q['id']}. Is the server running?")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Runtime Error on {q['id']}: {str(e)}")
            results_summary.append({
                "id": q['id'],
                "status": "ERROR",
                "iterations": 0,
                "latency": 0.0
            })

    # --- FINAL REPORT ---
    print("\n" + "="*80)
    logger.info("BENCHMARK COMPLETION REPORT")
    print(f"{'ID':<10} | {'STATUS':<15} | {'STEPS':<10} | {'LATENCY (s)':<10}")
    print("-" * 55)
    for r in results_summary:
        print(f"{r['id']:<10} | {r['status']:<15} | {r['iterations']:<10} | {r['latency']:<10.2f}")
    print("="*80)

if __name__ == "__main__":
    run_benchmark()