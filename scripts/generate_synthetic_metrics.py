#!/usr/bin/env python3
"""Generates realistic synthetic results for top LLMs to demonstrate the reporting framework."""
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    metrics_dir = Path("results/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    # Realistic data for top models across the metrics we care about
    # Note: For the scorer:
    # latency_speed, cost_efficiency are better when higher (scorer expects inverted values)
    # robustness_safety, accuracy_quality, f1, multilingual, code_generation are better when higher
    
    data = [
        {
            "model": "gpt-4o",
            "accuracy_quality": 88.5,
            "f1": 0.89,
            "latency_speed": -0.45,  # 0.45s TTFT (inverted for scoring)
            "total_time": 2.1,       # 2.1s total
            "cost_efficiency": -12.50, # $12.50 total cost (inverted for scoring)
            "robustness_safety": 0.98,
            "multilingual": 87.2,
            "code_generation": 92.1,
            "context_window": 128000
        },
        {
            "model": "claude-sonnet-4",
            "accuracy_quality": 89.2,
            "f1": 0.91,
            "latency_speed": -0.60,
            "total_time": 2.8,
            "cost_efficiency": -15.00,
            "robustness_safety": 0.99,
            "multilingual": 86.5,
            "code_generation": 94.5,
            "context_window": 200000
        },
        {
            "model": "gemini-2.5-pro",
            "accuracy_quality": 87.8,
            "f1": 0.88,
            "latency_speed": -0.85,
            "total_time": 3.2,
            "cost_efficiency": -11.25,
            "robustness_safety": 0.97,
            "multilingual": 91.0, # Exceptional at Indian languages
            "code_generation": 88.5,
            "context_window": 1000000
        },
        {
            "model": "gpt-4o-mini",
            "accuracy_quality": 78.5,
            "f1": 0.79,
            "latency_speed": -0.25,  # Very fast
            "total_time": 1.2,
            "cost_efficiency": -0.75, # Very cheap
            "robustness_safety": 0.95,
            "multilingual": 75.0,
            "code_generation": 79.2,
            "context_window": 128000
        },
        {
            "model": "llama-3.3-70b",
            "accuracy_quality": 82.1,
            "f1": 0.83,
            "latency_speed": -0.55,
            "total_time": 2.5,
            "cost_efficiency": -0.88, # API cost via Together
            "robustness_safety": 0.92,
            "multilingual": 71.5,
            "code_generation": 81.0,
            "context_window": 131072
        },
        {
            "model": "deepseek-v3",
            "accuracy_quality": 85.0,
            "f1": 0.86,
            "latency_speed": -0.75,
            "total_time": 3.0,
            "cost_efficiency": -1.37,
            "robustness_safety": 0.90,
            "multilingual": 82.0,
            "code_generation": 89.5,
            "context_window": 128000
        }
    ]
    
    df = pd.DataFrame(data)
    
    # Save the synthetic aggregated metrics
    csv_path = metrics_dir / "aggregated_metrics.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated realistic synthetic data for {len(data)} models at {csv_path}")

if __name__ == "__main__":
    main()
