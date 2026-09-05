---
license: apache-2.0
language:
- en
base_model:
- Qwen/Qwen3-4B-Instruct-2507
pipeline_tag: text-generation
tags:
- reasoning
- planning
- agent
- long-horizon
- adaptive
- goal-driven
---

# Eunoia-4B-Mini

## Model Details

### Model Description

**Eunoia-4B-Mini** is a lightweight but advanced reasoning-focused language model designed to improve **long-horizon coherence, goal tracking, and adaptive problem solving**.

Unlike conventional instruction-tuned models that operate in a single-pass generation loop, Eunoia introduces an **external cognitive control layer** that enables:

- Explicit goal hierarchies
- Step-wise evaluation and retry logic
- Adaptive goal mutation under failure
- Controlled advancement or abandonment of reasoning paths

The result is a model that remains compact (~4B parameters) while exhibiting **strong multi-step reasoning stability** and **reduced derailment over long outputs**.

This release is intended as a **research-oriented open-source baseline** for goal-driven and agentic LLM systems.

- **Developed by:** SHV Groups Pvt. Ltd.
- **Model type:** Decoder-only transformer with external reasoning controller
- **Language(s):** English
- **License:** Apache 2.0
- **Finetuned from:** Qwen/Qwen3-4B-Instruct-2507

---
## How Eunoia-4B-Mini Works (Detailed)

Eunoia-4B-Mini extends a standard instruction-tuned transformer with an **explicit external reasoning controller** designed to improve performance on long-horizon and multi-step tasks.

Instead of relying solely on implicit token-level reasoning, Eunoia separates *what to do* from *how to generate text* through a structured control loop:

1. **Goal Formation**  
   User instructions are interpreted as high-level goals that may be decomposed into sub-goals arranged in a hierarchical goal tree.

2. **Step Execution**  
   The base language model generates candidate outputs for the currently active goal.

3. **Semantic Evaluation**  
   Each output is evaluated for semantic sufficiency relative to the goal, determining whether the objective has been meaningfully satisfied.

4. **Execution Gating**  
   Based on evaluation results, the system decides whether to advance, retry, or abandon the current goal.

5. **Adaptive Goal Mutation**  
   If repeated failures occur, the system modifies the goal structure itself—splitting, simplifying, or reframing objectives instead of looping on the same prompt.

This process allows Eunoia to maintain coherence across longer reasoning chains and recover gracefully from partial failures.

---

## Design Philosophy

Eunoia-4B-Mini is built around three core principles:

- **Explicit Control over Implicit Guessing**  
  Reasoning structure is represented explicitly rather than being hidden inside token probabilities.

- **Adaptive Recovery instead of Blind Retry**  
  Failure is treated as a signal to restructure goals, not simply regenerate outputs.

- **Transparency and Modularity**  
  All reasoning components (goal trees, evaluators, gates, mutation logic) are external, inspectable, and replaceable.

This makes Eunoia suitable for research on agentic systems, planning, and long-horizon reasoning.

---

## Comparison with Standard Instruction-Tuned LLMs

| Aspect | Standard LLMs | Eunoia-4B-Mini |
|------|---------------|----------------|
| Reasoning flow | Single-pass generation | Multi-step controlled loop |
| Failure handling | Regenerate output | Evaluate → retry → mutate |
| Goal awareness | Implicit | Explicit goal hierarchy |
| Long-horizon stability | Degrades with length | Maintained via control logic |
| Agent readiness | Limited | Native support |

Eunoia does not replace the transformer; it **orchestrates it**.


---
## Model Sources

- **Repository:** https://huggingface.co/shvgroups/Eunoia-4B-mini
- **Paper:** Coming soon
- **Demo:** Coming soon

---

## Uses

### Direct Use

Eunoia-4B-Mini can be used directly for:

- Long-form explanations and essays
- Multi-step reasoning tasks
- Educational content generation
- Structured problem solving
- Agent-style workflows with external controllers
- Research on planning, retry, and adaptive reasoning loops

The model works with standard `text-generation` pipelines and does **not** require special token formats.

---

### Downstream Use

Eunoia-4B-Mini is particularly suitable for downstream systems such as:

- Autonomous or semi-autonomous agents
- Planner–executor architectures
- Tool-augmented reasoning systems
- Goal-conditioned fine-tuning
- Research into long-horizon alignment and stability

---

### Out-of-Scope Use

This model is **not designed** for:

- Safety-critical decision making
- Medical, legal, or financial advice
- Fully autonomous real-world control systems
- Use cases requiring formal guarantees or verification

---

## Bias, Risks, and Limitations

Like all large language models, Eunoia-4B-Mini may:

- Produce incorrect or misleading information
- Reflect biases present in its base model and training data
- Fail on tasks requiring real-time knowledge or sensory grounding

While the goal-control system improves structural reasoning, it does **not guarantee correctness**.

---

### Recommendations

Users are encouraged to:

- Combine the model with external verification where correctness matters
- Monitor outputs in autonomous or agentic settings
- Fine-tune or constrain the model for domain-specific use cases

---

## How to Get Started with the Model

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("shvgroups/Eunoia-4B-mini")
model = AutoModelForCausalLM.from_pretrained("shvgroups/Eunoia-4B-mini")

prompt = "Explain photosynthesis step by step."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

```


## Training Details

### Training Data

Eunoia-4B-Mini is built on top of the base model’s training corpus and further refined through:

- Instruction-following supervision  
- Reasoning-structured prompts  
- Iterative evaluation and retry loops  
- Goal-decomposition templates  

No private or user data was used in training or refinement.


### Training Procedure

#### Training Hyperparameters

- **Training regime:** Mixed-precision fine-tuning (fp16 / bf16)  
- **Architecture:** Decoder-only transformer with an external reasoning controller  

---

## Evaluation

### Metrics

The model is evaluated primarily on the following qualitative and behavioral metrics:

- Long-horizon coherence  
- Instruction adherence over extended outputs  
- Multi-step reasoning stability  
- Retry and recovery behavior under failure  

Formal benchmark results will be released in future updates.

---

## Environmental Impact

- **Hardware:** NVIDIA GPUs  
- **Training setup:** Research-scale fine-tuning  
- **Carbon impact:** Not formally measured  

---

## Technical Specifications

### Model Architecture and Objective

- **Base transformer:** Qwen3-4B-Instruct  

- **External reasoning modules:**
  - Goal Tree  
  - Execution Gate  
  - Goal Evaluator  
  - Adaptive Goal Mutation Engine  

These components operate outside the core transformer and guide generation iteratively through structured goal management and adaptive control logic.

---

## Citation

If you use this model in academic work, please cite:

### BibTeX

```bibtex
@misc{eunoia4bmini2025,
  title={Eunoia-4B-Mini: Goal-Driven Long-Horizon Reasoning},
  author={SHV Groups},
  year={2025},
  url={https://huggingface.co/shvgroups/Eunoia-4B-mini}
}
```
Authors
SHV Groups Research Team
