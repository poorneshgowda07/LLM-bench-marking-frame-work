# Detailed Performance Report: Codestral

**Model ID:** `codestral`  
**Provider:** Mistral  
**Parameters:** 22B  
**Context Window:** 32,768 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **Codestral** across 7 distinct task categories. 
The model achieved a general accuracy score of **79.0/100**, demonstrating its capabilities in this specific configuration tier.

---

## 2. Capability Matrix

| Feature | Supported |
| :--- | :---: |
| **Vision (Multimodal)** | ❌ |
| **Audio (Multimodal)** | ❌ |
| **Function Calling / Tools** | ❌ |
| **Native JSON Mode** | ❌ |
| **Chain-of-Thought Reasoning** | ❌ |

---

## 3. Benchmarking Performance Metrics

### A. Intelligence & Accuracy
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **General Accuracy (EM)** | **79.0%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.800** | Semantic overlap with reference answers. |
| **Code Generation** | **74.2%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **73.4%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.461 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **2.98 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **97.4%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$3.89** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Highly efficient execution speed.
* Well-rounded generalist model.
* Industry-leading speed (TTFT < 0.5s) ideal for real-time voice applications.

**Known Limitations:**
* Code-only, not suitable for general tasks
* No function calling or JSON mode

---
*Report generated automatically by the LLM Benchmarking Framework.*
