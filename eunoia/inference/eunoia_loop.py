from typing import Dict, Any, List, Set

from eunoia.core.intent_encoder import IntentEncoder
from eunoia.core.constraint_parser import ConstraintGraphBuilder
from eunoia.core.constraint_evaluator import ConstraintEvaluator
from eunoia.core.correction_policy import CorrectionPolicy
from eunoia.inference.base_model import BaseModel
from eunoia.memory.memory_store import MemoryStore


class EunoiaController:
    """
    EUNOIA COGNITIVE CONTROL LOOP (LEVEL 4)

    Capabilities:
    - Intent understanding
    - Constraint formalization
    - Constraint evaluation
    - Directed self-correction
    - Persistent learning from success
    - Deterministic termination
    """

    def __init__(
        self,
        model: BaseModel,
        max_iters: int = 3,
        stop_on_repeat: bool = True,
        enable_memory: bool = True,
    ):
        self.model = model
        self.max_iters = max_iters
        self.stop_on_repeat = stop_on_repeat
        self.enable_memory = enable_memory

        # Core cognition modules
        self.intent_encoder = IntentEncoder()
        self.graph_builder = ConstraintGraphBuilder()
        self.evaluator = ConstraintEvaluator()
        self.correction_policy = CorrectionPolicy()

        # Persistent memory (Level 4)
        self.memory = MemoryStore() if enable_memory else None

    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Execute Eunoia-controlled reasoning.

        Returns:
            {
                "final_output": str,
                "iterations": int,
                "history": List[dict],
                "memory_hit": bool,
                "terminated_reason": str | None
            }
        """

        history: List[Dict[str, Any]] = []
        seen_violation_signatures: Set[str] = set()
        terminated_reason = None
        memory_hit = False

        # 1. Encode intent + constraints
        frame = self.intent_encoder.encode(prompt)
        graph = self.graph_builder.build(frame.constraints)

        # 2. Memory retrieval (Level 4)
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

        # 3. Iterative control loop
        for iteration in range(self.max_iters):
            output = self.model.generate(current_prompt)

            eval_result = self.evaluator.evaluate(graph, output)
            violations = eval_result["violations"]
            is_compliant = eval_result["is_compliant"]

            history.append({
                "iteration": iteration + 1,
                "prompt": current_prompt,
                "output": output,
                "violations": violations,
                "compliant": is_compliant,
            })

            # 4. Stop if compliant
            if is_compliant:
                # 5. Persist successful experience (Level 4 learning)
                if self.enable_memory:
                    self.memory.add({
                        "task_signature": frame.intent_type,
                        "intent": frame.intent_type,
                        "constraints": frame.constraints,
                        "successful_prompt": current_prompt,
                        "successful_output": output,
                        "iterations_needed": iteration + 1,
                    })

                return {
                    "final_output": output,
                    "iterations": iteration + 1,
                    "history": history,
                    "memory_hit": memory_hit,
                    "terminated_reason": None,
                }

            # 6. Loop safety: repeated failure detection
            violation_signature = "|".join(sorted(violations))
            if (
                self.stop_on_repeat
                and violation_signature in seen_violation_signatures
            ):
                terminated_reason = "repeated_violation_pattern"
                break

            seen_violation_signatures.add(violation_signature)

            # 7. Directed correction (Phase B.3)
            current_prompt = self.correction_policy.build_correction_prompt(
                original_prompt=prompt,
                last_output=output,
                violations=violations,
            )

            last_output = output

        # 8. Termination without compliance
        if terminated_reason is None:
            terminated_reason = "max_iterations_reached"

        return {
            "final_output": last_output,
            "iterations": len(history),
            "history": history,
            "memory_hit": memory_hit,
            "terminated_reason": terminated_reason,
        }
