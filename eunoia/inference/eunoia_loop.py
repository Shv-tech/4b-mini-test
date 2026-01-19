from typing import Dict, Any, List, Set
from .crsto import CRSTO  # <--- CRSTO MODULE INTEGRATION
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
    Updated with CRSTO (Compute-Risk-Sparsity Tradeoff Objective) for dynamic efficiency.
    """

    def __init__(
        self,
        model: BaseModel,
        max_iters: int = 12,
        stop_on_repeat: bool = True,
        enable_memory: bool = True,
        confidence_threshold=0.85,
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
        
        # --- RESEARCH MODULE: CRSTO ---
        # Implementation of Compute-Risk-Sparsity Tradeoff Objective [Verma, 2025]
        # This module calculates the "Cost of Thinking" vs "Utility of Answer"
        # to enable dynamic halting (Efficiency Boost).
        self.crsto = CRSTO(kappa=0.02, beta=1.5) 

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

    def _finalize(self, output, iteration, history, confidence, reason):
        """
        Helper to construct the final return object.
        """
        return {
            "final_output": output,
            "iterations": iteration + 1,
            "history": history,
            "confidence": confidence,
            "terminated_reason": reason
        }

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

            # --- CRSTO OBJECTIVE EVALUATION [Verma, 2025] ---
            # Calculate the trade-off score for this step using the CRSTO formula.
            # Score = (s * U) / (1 + kappa * C_attn + beta * Risk)
            crsto_score = self.crsto.calculate_score(
                confidence=confidence, 
                iteration=iteration + 1, 
                token_count=len(output)
            )
            
            # Log CRSTO metrics for debugging/benchmark analysis
            print(f"   📊 CRSTO Score: {crsto_score:.4f} (Conf={confidence:.2f}, Cost={(iteration+1)**2})")

            # --- DECISION GATES ---
            
            # GATE 1: Verification Bypass (The Gold Standard)
            # If logic is verified by LHR, we stop immediately regardless of iteration count.
            if is_compliant and is_logically_sound:
                if self.enable_memory:
                     self._save_to_memory(frame, current_prompt, output, iteration)
                return self._finalize(output, iteration, history, confidence, "logic_verified")

            # GATE 2: CRSTO High-Value Halt (Efficiency Trigger)
            # If the CRSTO score is high (> 0.6), it means we have high utility relative to cost.
            # This allows early exit for easy problems without wasting compute.
            if is_compliant and crsto_score > 0.6:
                if self.enable_memory:
                     self._save_to_memory(frame, current_prompt, output, iteration)
                return self._finalize(output, iteration, history, confidence, "crsto_high_value")

            # GATE 3: CRSTO Diminishing Returns (The "Stop Wasting Time" Trigger)
            # If we are deep in the loop (iter > 4) and the score is tiny, the marginal utility
            # of thinking more is outweighed by the n^2 compute cost. Stop now.
            if iteration > 4 and crsto_score < 0.05:
                return self._finalize(output, iteration, history, confidence, "crsto_diminishing_returns")

            # GATE 4: Standard Confidence Threshold (Fallback)
            if is_compliant and confidence >= self.confidence_threshold:
                 if self.enable_memory:
                     self._save_to_memory(frame, current_prompt, output, iteration)
                 return self._finalize(output, iteration, history, confidence, "confidence_threshold")

            # 6. Correction Policy (If we didn't stop)
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

        return self._finalize(last_output, len(history), history, final_confidence, terminated_reason)

    def _save_to_memory(self, frame, current_prompt, output, iteration):
        """
        Helper to save successful traces to memory for future abstraction.
        """
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