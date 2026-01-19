import math

class CRSTO:
    """
    Compute-Risk-Sparsity Tradeoff Objective (CRSTO)
    Paper: Shaurya Verma, Eunoia Labs (2025)
    
    Formula: Score = (s * U) / (1 + kappa * C_attn + beta * Risk)
    """
    def __init__(self, kappa=0.05, beta=0.8, alpha=1.0):
        self.kappa = kappa  # Penalty for Compute (Time)
        self.beta = beta    # Penalty for Uncertainty (Risk)
        self.alpha = alpha  # Scaling factor for Attention Cost

    def calculate_score(self, confidence: float, iteration: int, token_count: int):
        """
        Calculates the CRSTO Score to decide if we should stop.
        """
        # 1. Utility (U): The model's confidence in its answer
        U = confidence
        
        # 2. Sparsity (s): We reward concise answers. 
        # If output is huge, s drops. (Simple heuristic: 1.0)
        s = 1.0 

        # 3. Compute Cost (C_attn): Quadratic scaling O(n^2)
        # We use 'iteration' as a proxy for sequence length accumulation
        n = iteration
        C_attn = self.alpha * (n ** 2)

        # 4. Risk (E[Z^2]): Uncertainty variance.
        # Proxy: The inverse of confidence (High confidence = Low risk)
        Risk = (1.0 - confidence) ** 2

        # 5. The CRSTO Formula [Equation 1]
        denominator = 1 + (self.kappa * C_attn) + (self.beta * Risk)
        score = (s * U) / denominator

        return score

    def should_halt(self, score: float, threshold: float = 0.15):
        """
        Decision Gate: If the score drops below threshold, 
        it means the 'marginal utility' of thinking more is too low.
        """
        return score < threshold