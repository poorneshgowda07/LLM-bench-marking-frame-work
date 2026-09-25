# Detailed Performance Report: GPT-4.1 mini

**Model ID:** `gpt-4.1-mini`  
**Provider:** Openai  
**Parameters:** ~20B  
**Context Window:** 1,000,000 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **GPT-4.1 mini** across 7 distinct task categories. 
The model achieved a general accuracy score of **89.0/100**, demonstrating its capabilities in this specific configuration tier.

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
| **General Accuracy (EM)** | **89.0%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.876** | Semantic overlap with reference answers. |
| **Code Generation** | **91.6%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **84.1%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.565 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **2.12 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **96.4%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$5.13** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Exceptional context window for massive document processing.
* Well-rounded generalist model.
* Reliable deep processing capabilities.

**Known Limitations:**
* No major structural limitations noted in this tier.

---
*Report generated automatically by the LLM Benchmarking Framework.*
