import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/v1/chat/completions"

def ask_eunoia(prompt, task_name="Test"):
    print(f"\n--- 🧪 TASK: {task_name} ---")
    print(f"📝 Prompt: {prompt}")
    
    payload = {
        "prompt": prompt,
        "max_iters": 12,        # Giving it time to think
        "confidence_threshold": 0.65
    }
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        duration = time.time() - start_time
        
        # Parse result
        answer = data["answer"]
        confidence = data["confidence"]
        steps = data["steps"]
        trace = data["thinking_trace"]
        
        print(f"🤖 Eunoia Answer: {answer}")
        print(f"🧠 Confidence: {confidence}")
        print(f"🔄 Steps Used: {steps}")
        print(f"⏱️ Time Taken: {duration:.2f}s")
        
        # Check if tools were used
        tool_uses = [t for t in trace if t.get("role") == "tool_execution"]
        if tool_uses:
            print(f"🛠️ Tool Used: Yes ({len(tool_uses)} times)")
            print(f"   Last Tool Output: {tool_uses[-1]['tool_output'][:100]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # 1. The Logic Test
    ask_eunoia(
        "If a rooster lays an egg on the roof, which way does it roll?", 
        "Logic Trap"
    )

    # 2. The Physics Test (The Big One)
    ask_eunoia(
        "Design a machine that transfers heat from 200K to 300K without external work.", 
        "Thermodynamics Check"
    )

    # 3. The Math Test (Requires Python Tool)
    ask_eunoia(
        "Calculate 25 * 48, then reverse the digits of the result.", 
        "Math & Tool Use"
    )