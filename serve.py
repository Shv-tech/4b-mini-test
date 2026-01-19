import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Import your Engine
from eunoia.inference.qwen_model import QwenModel
from eunoia.inference.eunoia_loop import EunoiaController

# --- API CONFIG ---
app = FastAPI(title="Eunoia 4B Omega API", version="5.0")

print("⏳ Loading Eunoia Brain (This takes a few seconds)...")
# 1. Load Model ONCE (Global State)
# We do this here so we don't reload 4GB of weights for every request
base_model = QwenModel() 
print("Eunoia System Online.")

# --- DATA MODELS ---
class QueryRequest(BaseModel):
    prompt: str
    max_iters: int = 12
    confidence_threshold: float = 0.65
    enable_memory: bool = True

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    steps: int
    thinking_trace: List[Dict[str, Any]]
    status: str

# --- ENDPOINTS ---
@app.get("/health")
def health_check():
    return {"status": "operational", "system": "Eunoia-Omega"}

@app.post("/v1/chat/completions", response_model=QueryResponse)
def generate(req: QueryRequest):
    """
    The Main Brain Endpoint.
    """
    try:
        # 2. Spin up a fresh Controller for this specific request
        # (The controller is lightweight; the model is heavy and shared)
        controller = EunoiaController(
            model=base_model,
            max_iters=req.max_iters,
            confidence_threshold=req.confidence_threshold,
            enable_memory=req.enable_memory
        )

        # 3. Run the Cognitive Loop
        result = controller.run(req.prompt)

        # 4. Format for the user
        return QueryResponse(
            answer=str(result.get("final_output", "")),
            confidence=float(result.get("confidence", 0.0)),
            steps=int(result.get("iterations", 0)),
            thinking_trace=result.get("history", []),
            status="success"
        )

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)