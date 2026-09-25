# Detailed Performance Report: Llama 4 Maverick

**Model ID:** `llama-4-maverick`  
**Provider:** Meta  
**Parameters:** 400B (17B active, MoE)  
**Context Window:** 131,072 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **Llama 4 Maverick** across 7 distinct task categories. 
The model achieved a general accuracy score of **87.1/100**, demonstrating its capabilities in this specific configuration tier.

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
| **General Accuracy (EM)** | **87.1%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.891** | Semantic overlap with reference answers. |
| **Code Generation** | **88.2%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **84.9%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.731 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **3.64 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **85.2%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$10.25** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Highly efficient execution speed.
* Well-rounded generalist model.
* Reliable deep processing capabilities.

**Known Limitations:**
* Requires Together AI or local Ollama

---
*Report generated automatically by the LLM Benchmarking Framework.*
