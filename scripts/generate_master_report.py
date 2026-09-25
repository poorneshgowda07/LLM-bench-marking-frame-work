#!/usr/bin/env python3
"""Generates a single, simple, easy-to-understand master report for all models."""
import pandas as pd
import yaml
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    metrics_path = Path("results/metrics/aggregated_metrics.csv")
    if not metrics_path.exists():
        print("Metrics file not found.")
        sys.exit(1)
        
    df = pd.read_csv(metrics_path)
    df.set_index("model", inplace=True)
    
    with open("configs/models.yaml") as f:
        models_config = yaml.safe_load(f)["models"]
        
    report = """# 🏆 LLM Benchmark: Master Report

Welcome to the simplified, all-in-one performance report for the 23 models tested in our framework. 
This report breaks down the complex metrics into an easy-to-understand guide so you can quickly choose the right model for your task.

---

## 🌟 Category Winners (At a Glance)

"""
    # Calculate winners
    df["latency_s"] = -df["latency_speed"]
    df["cost_usd"] = -df["cost_efficiency"]
    
    best_overall = df["accuracy_quality"].idxmax()
    fastest = df[df.index != "mock"]["latency_s"].idxmin()
    cheapest = df[(df.index != "mock") & (df["cost_usd"] > 0)]["cost_usd"].idxmin()
    best_code = df["code_generation"].idxmax()
    best_indic = df["multilingual"].idxmax()
    
    report += f"""* **🧠 Smartest Overall:** `{best_overall}` (Highest general accuracy)
* **⚡ Fastest Responder:** `{fastest}` (Lowest Time-to-First-Token)
* **💰 Most Cost-Effective:** `{cheapest}` (Cheapest API cost per run)
* **💻 Best for Coding:** `{best_code}` (Highest code generation score)
* **🇮🇳 Best for Indian Languages:** `{best_indic}` (Highest multilingual score)

---

## 📊 Complete Model Comparison

Here is how all 23 models stack up against each other. 
*(Models are sorted by their General Accuracy)*

| Model Name | Provider | General Accuracy | Latency (TTFT) | Estimated Cost | Context Window |
| :--- | :--- | :---: | :---: | :---: | :---: |
"""
    
    # Sort by accuracy descending
    df_sorted = df.sort_values(by="accuracy_quality", ascending=False)
    
    for model_id, row in df_sorted.iterrows():
        if model_id not in models_config:
            continue
            
        config = models_config[model_id]
        display_name = config.get("display_name", model_id)
        provider = config.get("provider", "Unknown").capitalize()
        acc = f"{row['accuracy_quality']:.1f}%"
        lat = f"{row['latency_s']:.2f}s"
        cost = f"${row['cost_usd']:.2f}" if row['cost_usd'] > 0 else "Free / Local"
        ctx = f"{config.get('context_window', 0):,}"
        
        # Add emoji for reasoning models
        if config.get("reasoning_cot"):
            display_name += " 🧠"
            
        report += f"| **{display_name}** | {provider} | {acc} | {lat} | {cost} | {ctx} |\n"

    report += """
*Note: Models with a 🧠 icon are "Reasoning" models (like OpenAI's o3 or DeepSeek-R1) which "think" before they answer. They are smarter but usually slower.*

---

## 💡 How to Choose?

* **Building a Chatbot?** Pick a model with low latency (like `gpt-4o-mini` or `gemini-2.5-flash`).
* **Writing Complex Code?** Pick `claude-sonnet-4` or `gpt-4o`.
* **Analyzing Huge Documents?** Pick `gemini-2.5-pro` for its massive 1,000,000 token context window.
* **Saving Money?** Look at open-weight models like `llama-3.3-70b` or `deepseek-v3` which offer near-frontier intelligence at a fraction of the cost.

"""
    
    output_path = Path("MASTER_REPORT.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Generated single master report at {output_path}")

if __name__ == "__main__":
    main()
