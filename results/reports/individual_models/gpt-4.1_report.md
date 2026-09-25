# Detailed Performance Report: GPT-4.1

**Model ID:** `gpt-4.1`  
**Provider:** Openai  
**Parameters:** ~200B  
**Context Window:** 1,000,000 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **GPT-4.1** across 7 distinct task categories. 
The model achieved a general accuracy score of **84.2/100**, demonstrating its capabilities in this specific configuration tier.

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
| **General Accuracy (EM)** | **84.2%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.844** | Semantic overlap with reference answers. |
| **Code Generation** | **82.3%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **75.1%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.473 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **2.67 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **97.0%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$8.60** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Exceptional context window for massive document processing.
* Well-rounded generalist model.
* Industry-leading speed (TTFT < 0.5s) ideal for real-time voice applications.

**Known Limitations:**
* Knowledge cutoff June 2025

---
*Report generated automatically by the LLM Benchmarking Framework.*
