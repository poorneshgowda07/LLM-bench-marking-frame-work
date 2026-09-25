# Detailed Performance Report: Mock LLM (Testing)

**Model ID:** `mock`  
**Provider:** Mock  
**Parameters:** N/A  
**Context Window:** 999,999 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **Mock LLM (Testing)** across 7 distinct task categories. 
The model achieved a general accuracy score of **0.0/100**, demonstrating its capabilities in this specific configuration tier.

---

## 2. Capability Matrix

| Feature | Supported |
| :--- | :---: |
| **Vision (Multimodal)** | ✅ |
| **Audio (Multimodal)** | ✅ |
| **Function Calling / Tools** | ✅ |
| **Native JSON Mode** | ✅ |
| **Chain-of-Thought Reasoning** | ✅ |

---

## 3. Benchmarking Performance Metrics

### A. Intelligence & Accuracy
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **General Accuracy (EM)** | **0.0%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.000** | Semantic overlap with reference answers. |
| **Code Generation** | **0.3%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **0.0%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.100 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **2.58 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **90.0%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$0.00** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Exceptional context window for massive document processing.
* Strong native reasoning capabilities due to integrated Chain-of-Thought.
* Industry-leading speed (TTFT < 0.5s) ideal for real-time voice applications.

**Known Limitations:**
* Returns deterministic mock responses
* Not suitable for real evaluation

---
*Report generated automatically by the LLM Benchmarking Framework.*
