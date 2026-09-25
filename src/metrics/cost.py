"""Cost metrics calculation."""
from typing import List, Dict

def calculate_cost_metrics(costs_usd: List[float], input_tokens: List[int], output_tokens: List[int]) -> Dict[str, float]:
    if not costs_usd:
        return {}
        
    total_cost = sum(costs_usd)
    total_input = sum(input_tokens)
    total_output = sum(output_tokens)
    
    avg_cost_per_query = total_cost / len(costs_usd)
    
    # Cost per 1K tokens
    total_tokens = total_input + total_output
    if total_tokens > 0:
        cost_per_1k_tokens = (total_cost / total_tokens) * 1000
    else:
        cost_per_1k_tokens = 0.0
        
    return {
        "total_cost_usd": total_cost,
        "avg_cost_per_query": avg_cost_per_query,
        "cost_per_1k_tokens": cost_per_1k_tokens,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output
    }
