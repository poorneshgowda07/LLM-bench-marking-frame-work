#!/usr/bin/env python3
"""Calculates metrics from raw results."""
import sys
import json
import pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.metrics.accuracy import calculate_accuracy_metrics
from src.utils.logger import logger

def main():
    logger.info("Calculating metrics...")
    raw_dir = Path("results/raw")
    metrics_dir = Path("results/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = []
    
    if not raw_dir.exists():
        logger.warning(f"No raw results found in {raw_dir}")
        return
        
    for file_path in raw_dir.rglob("*.json"):
        try:
            with open(file_path) as f:
                res = json.load(f)
                
            prediction = res["response"].get("prediction", "")
            reference = res.get("reference", "")
            if isinstance(reference, dict):
                reference = json.dumps(reference)
                
            metrics = calculate_accuracy_metrics(prediction, reference)
            
            row = {
                "model": res["model"],
                "task_category": res["task_category"],
                "sample_id": res["sample_id"],
                "ttft": res["response"].get("ttft", 0),
                "total_time": res["response"].get("total_time", 0),
                "cost": res["response"].get("cost_usd", 0),
                "is_error": res["response"].get("is_error", False)
            }
            row.update(metrics)
            all_results.append(row)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            
    if all_results:
        df = pd.DataFrame(all_results)
        # Aggregate by model
        # Note: mapping exact metrics to scoring config column names
        agg_df = df.groupby("model").agg({
            "exact_match": "mean",
            "f1": "mean",
            "ttft": "mean",
            "total_time": "mean",
            "cost": "sum",
            "is_error": "mean"
        }).reset_index()
        
        # Rename for scorer
        agg_df = agg_df.rename(columns={
            "exact_match": "accuracy_quality",
            "ttft": "latency_speed", 
            "cost": "cost_efficiency",
            "is_error": "robustness_safety"
        })
        
        # Add dummy columns for other required metrics for scorer
        agg_df["multilingual"] = agg_df["accuracy_quality"]
        agg_df["code_generation"] = agg_df["accuracy_quality"]
        agg_df["context_window"] = 1.0
        
        # Invert metrics where lower is better so higher=better for scorer
        agg_df["latency_speed"] = -agg_df["latency_speed"]
        agg_df["cost_efficiency"] = -agg_df["cost_efficiency"]
        agg_df["robustness_safety"] = 1.0 - agg_df["robustness_safety"]
        
        agg_df.to_csv(metrics_dir / "aggregated_metrics.csv", index=False)
        logger.info(f"Saved metrics for {len(agg_df)} models.")
    else:
        logger.info("No results to process.")

if __name__ == "__main__":
    main()
