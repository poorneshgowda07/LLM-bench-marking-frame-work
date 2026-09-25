#!/usr/bin/env python3
"""Generates detailed individual markdown reports for every single model."""
import pandas as pd
import yaml
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    metrics_path = Path("results/metrics/aggregated_metrics.csv")
    reports_dir = Path("results/reports/individual_models")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    if not metrics_path.exists():
        print("Metrics file not found. Run calculate_metrics or generate_synthetic_metrics first.")
        sys.exit(1)
        
    df = pd.read_csv(metrics_path)
    df.set_index("model", inplace=True)
    
    with open("configs/models.yaml") as f:
        models_config = yaml.safe_load(f)["models"]
        
    for model_id, config in models_config.items():
        if model_id not in df.index:
            continue
            
        metrics = df.loc[model_id]
        
        # Format the metrics (handling inverted metrics)
        ttft = -metrics["latency_speed"]
        cost = -metrics["cost_efficiency"]
        
        report = f"""# Detailed Performance Report: {config['display_name']}

**Model ID:** `{model_id}`  
**Provider:** {config['provider'].capitalize()}  
**Parameters:** {config.get('parameters', 'N/A')}  
**Context Window:** {config.get('context_window', 'N/A'):,} tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **{config['display_name']}** across 7 distinct task categories. 
The model achieved a general accuracy score of **{metrics['accuracy_quality']:.1f}/100**, demonstrating its capabilities in this specific configuration tier.

---

## 2. Capability Matrix

| Feature | Supported |
| :--- | :---: |
| **Vision (Multimodal)** | {'✅' if config['multimodal'].get('vision') else '❌'} |
| **Audio (Multimodal)** | {'✅' if config['multimodal'].get('audio') else '❌'} |
| **Function Calling / Tools** | {'✅' if config.get('function_calling') else '❌'} |
| **Native JSON Mode** | {'✅' if config.get('json_mode') else '❌'} |
| **Chain-of-Thought Reasoning** | {'✅' if config.get('reasoning_cot') else '❌'} |

---

## 3. Benchmarking Performance Metrics

### A. Intelligence & Accuracy
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **General Accuracy (EM)** | **{metrics['accuracy_quality']:.1f}%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **{metrics['f1']:.3f}** | Semantic overlap with reference answers. |
| **Code Generation** | **{metrics['code_generation']:.1f}%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **{metrics['multilingual']:.1f}%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **{ttft:.3f} s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **{metrics['total_time']:.2f} s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **{(metrics['robustness_safety'] * 100):.1f}%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **${cost:.2f}** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* {'Exceptional context window for massive document processing.' if config.get('context_window', 0) >= 200000 else 'Highly efficient execution speed.'}
* {'Strong native reasoning capabilities due to integrated Chain-of-Thought.' if config.get('reasoning_cot') else 'Well-rounded generalist model.'}
* {'Industry-leading speed (TTFT < 0.5s) ideal for real-time voice applications.' if ttft < 0.5 else 'Reliable deep processing capabilities.'}

**Known Limitations:**
"""
        for limitation in config.get('limitations', []):
            report += f"* {limitation}\n"
            
        if not config.get('limitations'):
            report += "* No major structural limitations noted in this tier.\n"
            
        report += "\n---\n*Report generated automatically by the LLM Benchmarking Framework.*\n"
        
        # Save report
        report_file = reports_dir / f"{model_id}_report.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
            
    print(f"Generated {len(models_config)} individual model reports in {reports_dir}")

if __name__ == "__main__":
    main()
