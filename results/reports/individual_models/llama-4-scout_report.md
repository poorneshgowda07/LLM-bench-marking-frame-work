# Detailed Performance Report: Llama 4 Scout

**Model ID:** `llama-4-scout`  
**Provider:** Meta  
**Parameters:** 109B (17B active, MoE)  
**Context Window:** 131,072 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **Llama 4 Scout** across 7 distinct task categories. 
The model achieved a general accuracy score of **75.3/100**, demonstrating its capabilities in this specific configuration tier.

---

## 2. Capability Matrix

| Feature | Supported |
| :--- | :---: |
| **Vision (Multimodal)** | ✅ |
| **Audio (Multimodal)** | ❌ |
| **Function Calling / Tools** | ✅ |
| **Native JSON Mode** | ✅ |
| **Chain-of-Thought Reasoning** | ❌ |

---

## 3. Benchmarking Performance Metrics

### A. Intelligence & Accuracy
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **General Accuracy (EM)** | **75.3%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.752** | Semantic overlap with reference answers. |
| **Code Generation** | **75.7%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **66.2%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.993 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **3.84 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **98.8%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$3.84** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Highly efficient execution speed.
* Well-rounded generalist model.
* Reliable deep processing capabilities.

**Known Limitations:**
* Requires Together AI or local Ollama for API access

---
*Report generated automatically by the LLM Benchmarking Framework.*
