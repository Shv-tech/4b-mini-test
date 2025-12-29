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

class EunoiaController:
    """
    EUNOIA COGNITIVE CONTROL LOOP (LEVEL 4 → 4.5)

    Upgraded capabilities:
    - Intent understanding
    - Constraint formalization
    - Constraint evaluation
    - Directed self-correction
    - Persistent learning from success
    - Deterministic termination
    - Meta-confidence tracking (logic-first)
    """

    def __init__(
        self,
        model: BaseModel,
        max_iters: int = 3,
        stop_on_repeat: bool = True,
        enable_memory: bool = True,
        confidence_threshold: float = 0.65,
    ):
        self.model = model
        self.max_iters = max_iters
        self.stop_on_repeat = stop_on_repeat
        self.enable_memory = enable_memory
        self.confidence_threshold = confidence_threshold

        # Core cognition modules (unchanged)
        self.intent_encoder = IntentEncoder()
        self.graph_builder = ConstraintGraphBuilder()
        self.evaluator = ConstraintEvaluator()
        self.correction_policy = CorrectionPolicy()

        # Persistent memory (Level 4)
        self.memory = MemoryStore() if enable_memory else None

    # --------------------------------------------------
    # Internal analysis utilities (LOGIC FIRST)
    # --------------------------------------------------


    def _estimate_confidence(
        self,
        eval_result: Dict[str, Any],
        iteration: int,
    ) -> float:
        """
        Conservative confidence estimator.
        Logic > fluency.
        """
        if eval_result["is_compliant"]:
            # Earlier compliance → higher confidence
            return max(0.7, 1.0 - (iteration * 0.15))

        violations = eval_result.get("violations", [])
        if not violations:
            return 0.6

        penalty = min(len(violations) * 0.15, 0.6)
        return max(0.2, 0.6 - penalty)

    def _classify_failure(self, violations) -> str:
        """
        Structured failure typing (for future ESR / science routing)
        """
        if not violations:
            return "unknown"

        sigs = [v.signature.lower() for v in violations]

        if any("steps" in s or "count" in s for s in sigs):
            return "procedural_logic"
        if any("unit" in s or "format" in s for s in sigs):
            return "representation_error"
        if any("constraint" in s for s in sigs):
            return "constraint_violation"

        return "general_logic_failure"

    # --------------------------------------------------
    # Main reasoning loop
    # --------------------------------------------------

    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Execute Eunoia-controlled reasoning.

        Returns:
            {
                "final_output": str,
                "iterations": int,
                "history": List[dict],
                "confidence": float,
                "memory_hit": bool,
                "terminated_reason": str | None
            }
        """

        history: List[Dict[str, Any]] = []
        seen_violation_signatures: Set[str] = set()
        terminated_reason = None
        memory_hit = False
        final_confidence = 0.0

        # 1. Encode intent + constraints
        frame = self.intent_encoder.encode(prompt)
        graph = self.graph_builder.build(frame.constraints)

        # 2. Memory retrieval (unchanged)
        current_prompt = frame.content
        if self.enable_memory:
            record = self.memory.find_similar(
                intent=frame.intent_type,
                constraints=frame.constraints,
            )
            if record:
                current_prompt = record["successful_prompt"]
                memory_hit = True

        last_output = None

        # 3. Iterative reasoning loop
        for iteration in range(self.max_iters):
            output = self.model.generate(current_prompt)

            eval_result = self.evaluator.evaluate(graph, output)
            violations = eval_result["violations"]
            is_compliant = eval_result["is_compliant"]

            confidence = self._estimate_confidence(
                eval_result=eval_result,
                iteration=iteration,
            )

            failure_type = self._classify_failure(violations)

            history.append({
                "iteration": iteration + 1,
                "prompt": current_prompt,
                "output": output,
                "violations": violations,
                "compliant": is_compliant,
                "confidence": confidence,
                "failure_type": failure_type,
            })

            final_confidence = confidence
            last_output = output

            # 4. Accept only if logically compliant AND confident
            if is_compliant and confidence >= self.confidence_threshold:
                signature = tuple(frame.domain + frame.heuristics_used)
                if self.enable_memory:
                    self.memory.add({
                        "task_signature": frame.intent_type,
                        "intent": frame.intent_type,
                        "constraints": frame.constraints,
                        "successful_prompt": current_prompt,
                        "successful_output": output,
                        "iterations_needed": iteration + 1,
                    })

                if abstraction_detector.observe(signature):
                    tool = tool_synthesizer.synthesize(signature)
                    tool_registry.add(tool)

                return {
                    "final_output": output,
                    "iterations": iteration + 1,
                    "history": history,
                    "confidence": confidence,
                    "memory_hit": memory_hit,
                    "terminated_reason": None,
                }

            # 5. Loop safety: repeated reasoning pattern
            violation_signature = "|".join(
                sorted(v.signature for v in violations)
            )

            if (
                self.stop_on_repeat
                and violation_signature in seen_violation_signatures
            ):
                terminated_reason = "repeated_violation_pattern"
                break

            seen_violation_signatures.add(violation_signature)

            # 6. Directed correction (unchanged, but now informed)
            current_prompt = self.correction_policy.build_correction_prompt(
                original_prompt=prompt,
                last_output=output,
                violations=violations,
            )

        # 7. Termination without full compliance
        if terminated_reason is None:
            terminated_reason = "max_iterations_reached"

        return {
            "final_output": last_output,
            "iterations": len(history),
            "history": history,
            "confidence": final_confidence,
            "memory_hit": memory_hit,
            "terminated_reason": terminated_reason,
        
    }