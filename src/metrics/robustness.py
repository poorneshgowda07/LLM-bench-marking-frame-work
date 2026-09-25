"""Robustness metrics: consistency, failure rate."""
from typing import List, Dict
import numpy as np

def calculate_robustness_metrics(errors: List[bool], consistencies: List[float] = None) -> Dict[str, float]:
    total = len(errors)
    if total == 0:
        return {}
        
    failure_rate = sum(errors) / total
    success_rate = 1.0 - failure_rate
    
    metrics = {
        "failure_rate": failure_rate,
        "success_rate": success_rate,
    }
    
    if consistencies and len(consistencies) > 0:
        metrics["consistency_score"] = float(np.mean(consistencies))
        
    return metrics
