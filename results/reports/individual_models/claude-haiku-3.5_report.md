# Detailed Performance Report: Claude Haiku 3.5

**Model ID:** `claude-haiku-3.5`  
**Provider:** Anthropic  
**Parameters:** ~20B  
**Context Window:** 200,000 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **Claude Haiku 3.5** across 7 distinct task categories. 
The model achieved a general accuracy score of **76.8/100**, demonstrating its capabilities in this specific configuration tier.

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
| **General Accuracy (EM)** | **76.8%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.771** | Semantic overlap with reference answers. |
| **Code Generation** | **80.7%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **80.4%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.311 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **2.16 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **95.4%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$0.54** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Exceptional context window for massive document processing.
* Well-rounded generalist model.
* Industry-leading speed (TTFT < 0.5s) ideal for real-time voice applications.

**Known Limitations:**
* Lower reasoning depth

---
*Report generated automatically by the LLM Benchmarking Framework.*
