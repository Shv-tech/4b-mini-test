from typing import Dict, Any, List, Set

from eunoia.core.intent_encoder import IntentEncoder
from eunoia.core.constraint_parser import ConstraintGraphBuilder
from eunoia.core.constraint_evaluator import ConstraintEvaluator
from eunoia.core.correction_policy import CorrectionPolicy
from eunoia.inference.base_model import BaseModel
from eunoia.memory.memory_store import MemoryStore
from eunoia.core.factor_extractor import FactorExtractor, FactorExtractionError
from eunoia.core.variable_graph import VariableGraph
from eunoia.meta.abstraction_detector import AbstractionDetector
from eunoia.meta.tool_synthesizer import ToolSynthesizer
from eunoia.meta.tool_registry import ToolRegistry
# IMPORTS: Connect the Logical Brain & Tools
from eunoia.lhr.lhr_omega import LHRomega
from eunoia.tools.python_sandbox import PythonSandbox 

class EunoiaController:
    """
    EUNOIA COGNITIVE CONTROL LOOP (LEVEL 5: OMEGA)
    """

    def __init__(
        self,
        model: BaseModel,
        max_iters: int = 12,  # <--- CHANGED: Increased from 5 to 12 (The "Deep Thought" Fix)
        stop_on_repeat: bool = True,
        enable_memory: bool = True,
        confidence_threshold: float = 0.65,
    ):
        self.model = model
        self.max_iters = max_iters
        self.stop_on_repeat = stop_on_repeat
        self.enable_memory = enable_memory
        self.confidence_threshold = confidence_threshold

        # Core cognition
        self.intent_encoder = IntentEncoder()
        self.graph_builder = ConstraintGraphBuilder()
        self.evaluator = ConstraintEvaluator()
        self.correction_policy = CorrectionPolicy()

        # Meta-Learning & Logic
        self.abstraction_detector = AbstractionDetector()
        self.tool_synthesizer = ToolSynthesizer()
        self.tool_registry = ToolRegistry()
        self.lhr = LHRomega()           # The Logical CPU
        self.sandbox = PythonSandbox()  # Initialize Sandbox

        self.memory = MemoryStore() if enable_memory else None

    def _estimate_confidence(self, eval_result: Dict[str, Any], iteration: int, logic_verified: bool = False) -> float:
        """
        Confidence is now boosted by Logical Verification.
        """
        base_score = 0.6 if not eval_result.get("violations") else 0.2
        
        if eval_result["is_compliant"]:
            base_score = 0.8
            
        # If the Logical CPU says it works, confidence skyrockets
        if logic_verified:
            return min(0.99, base_score + 0.2)
            
        return max(0.1, base_score - (iteration * 0.05)) # Slower decay for longer loops

    def _classify_failure(self, violations) -> str:
        if not violations: return "unknown"
        sigs = [v.signature.lower() for v in violations]
        if any("steps" in s or "count" in s for s in sigs): return "procedural_logic"
        if any("unit" in s or "format" in s for s in sigs): return "representation_error"
        return "general_logic_failure"

    def run(self, prompt: str) -> Dict[str, Any]:
        history = []
        seen_violation_signatures = set()
        terminated_reason = None
        memory_hit = False
        final_confidence = 0.0

        # 1. Encode Intent
        frame = self.intent_encoder.encode(prompt)
        graph = self.graph_builder.build(frame.constraints)

        # 1.5. Extract Reasoning Skeleton (The Variables)
        try:
            rts_factors = FactorExtractor.extract(prompt)
        except:
            rts_factors = {} 

        current_prompt = frame.content
        if self.enable_memory:
            record = self.memory.find_similar(intent=frame.intent_type, constraints=frame.constraints)
            if record:
                current_prompt = record["successful_prompt"]
                memory_hit = True

        # System Injection
        current_prompt += (
            "\n[SYSTEM]: You have a Python interpreter. "
            "To calculate or process data, write code in ```python ... ``` blocks. "
            "The system will execute it and give you the answer."
        )

        last_output = "" 

        for iteration in range(self.max_iters):
            output = self.model.generate(current_prompt)
            last_output = output # Capture output BEFORE tool execution

            # --- TOOL EXECUTION BLOCK ---
            tool_output = self.sandbox.execute(output)
            if tool_output:
                # If tool ran, we DON'T evaluate yet. We feed result back.
                history.append({
                    "iteration": iteration + 1,
                    "output": output,
                    "tool_output": tool_output,
                    "role": "tool_execution"
                })
                # Update confidence to show we are working
                final_confidence = 0.5 
                
                # Add observation and continue to next iteration immediately
                current_prompt += f"\n{output}\n[OBSERVATION]: {tool_output}\n"
                continue
            # -----------------------------

            # 2. Standard Evaluation (Formatting/Constraints)
            eval_result = self.evaluator.evaluate(graph, output)
            is_compliant = eval_result["is_compliant"]

            # 3. OMEGA STEP: Logical Verification
            is_logically_sound = False
            try:
                # Merge prompt factors with output for verification
                verification_context = {**rts_factors, "output": output}
                is_logically_sound = self.lhr.verify(verification_context)
            except Exception:
                is_logically_sound = False

            # 4. Confidence Calculation
            confidence = self._estimate_confidence(
                eval_result, 
                iteration, 
                logic_verified=is_logically_sound
            )

            history.append({
                "iteration": iteration + 1,
                "output": output,
                "compliant": is_compliant,
                "logically_verified": is_logically_sound,
                "confidence": confidence
            })

            final_confidence = confidence

            # 5. Acceptance Gate
            if is_compliant and (is_logically_sound or confidence >= self.confidence_threshold):
                
                if self.enable_memory:
                     self.memory.add({
                        "task_signature": frame.intent_type,
                        "intent": frame.intent_type,
                        "constraints": frame.constraints,
                        "successful_prompt": current_prompt,
                        "successful_output": output,
                        "iterations_needed": iteration + 1,
                    })
                
                signature = tuple([frame.intent_type] + frame.heuristics_used)
                if self.abstraction_detector.observe(signature):
                    tool = self.tool_synthesizer.synthesize(signature)
                    self.tool_registry.add(tool)

                return {
                    "final_output": output,
                    "iterations": iteration + 1,
                    "history": history,
                    "confidence": confidence,
                    "terminated_reason": None,
                }

            # 6. Correction Policy
            violation_signature = "|".join(sorted(v.signature for v in eval_result["violations"]))
            if self.stop_on_repeat and violation_signature in seen_violation_signatures:
                terminated_reason = "repeated_violation_pattern"
                break
            seen_violation_signatures.add(violation_signature)

            current_prompt = self.correction_policy.build_correction_prompt(
                original_prompt=prompt,
                last_output=output,
                violations=eval_result["violations"],
            )

        if terminated_reason is None:
            terminated_reason = "max_iterations_reached"

        return {
            "final_output": last_output,
            "iterations": len(history),
            "history": history,
            "confidence": final_confidence,
            "terminated_reason": terminated_reason,
        }