#!/usr/bin/env python3
"""Generates realistic synthetic results for ALL models to demonstrate the reporting framework."""
import pandas as pd
from pathlib import Path
import sys
import yaml
import random

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    metrics_dir = Path("results/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    # Load all models
    with open("configs/models.yaml") as f:
        models_config = yaml.safe_load(f)["models"]
        
    data = []
    for model_id, config in models_config.items():
        # Generate plausible metrics based on model size/type
        provider = config["provider"]
        params = str(config.get("parameters", "unknown"))
        is_mini = "mini" in model_id or "flash" in model_id or "haiku" in model_id or "small" in model_id or "nano" in model_id
        is_frontier = "4o" in model_id or "4.1" in model_id or "opus" in model_id or "sonnet" in model_id or "pro" in model_id or "v3" in model_id or "large" in model_id or "70b" in model_id or "maverick" in model_id
        is_reasoning = config.get("reasoning_cot", False) or "o3" in model_id or "o4" in model_id or "r1" in model_id
        
        # Base accuracy
        if is_reasoning:
            acc = random.uniform(90.0, 96.0)
            ttft = random.uniform(1.5, 5.0) # Reasoning takes longer
            cost = random.uniform(5.0, 20.0)
        elif is_frontier:
            acc = random.uniform(84.0, 91.0)
            ttft = random.uniform(0.4, 0.8)
            cost = random.uniform(2.0, 15.0)
        elif is_mini:
            acc = random.uniform(72.0, 81.0)
            ttft = random.uniform(0.15, 0.4)
            cost = random.uniform(0.1, 1.0)
        else:
            acc = random.uniform(75.0, 85.0)
            ttft = random.uniform(0.4, 1.0)
            cost = random.uniform(1.0, 5.0)
            
        if model_id == "mock":
            acc = 0.0
            ttft = 0.1
            cost = 0.0
            
        # Add some noise to specific metrics
        f1 = (acc / 100.0) + random.uniform(-0.02, 0.02)
        code = acc + random.uniform(-5.0, 5.0)
        multi = acc + random.uniform(-10.0, 5.0)
        if provider == "google": multi += 5.0 # Google bias for multilingual
        
        data.append({
            "model": model_id,
            "accuracy_quality": max(0, min(100, acc)),
            "f1": max(0, min(1.0, f1)),
            "latency_speed": -ttft,  # inverted for scorer
            "total_time": ttft + random.uniform(1.0, 3.0),
            "cost_efficiency": -cost, # inverted for scorer
            "robustness_safety": random.uniform(0.85, 0.99),
            "multilingual": max(0, min(100, multi)),
            "code_generation": max(0, min(100, code)),
            "context_window": config.get("context_window", 8192)
        })
        
    df = pd.DataFrame(data)
    csv_path = metrics_dir / "aggregated_metrics.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated realistic synthetic data for all {len(data)} models at {csv_path}")

if __name__ == "__main__":
    main()
