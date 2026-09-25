# Detailed Performance Report: GPT-4o mini

**Model ID:** `gpt-4o-mini`  
**Provider:** Openai  
**Parameters:** ~8B  
**Context Window:** 128,000 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **GPT-4o mini** across 7 distinct task categories. 
The model achieved a general accuracy score of **87.8/100**, demonstrating its capabilities in this specific configuration tier.

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
| **General Accuracy (EM)** | **87.8%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.878** | Semantic overlap with reference answers. |
| **Code Generation** | **90.9%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **80.1%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **0.565 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **3.18 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **98.8%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$6.62** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Highly efficient execution speed.
* Well-rounded generalist model.
* Reliable deep processing capabilities.

**Known Limitations:**
* Smaller context understanding vs GPT-4o

---
*Report generated automatically by the LLM Benchmarking Framework.*
