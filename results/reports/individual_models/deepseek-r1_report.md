# Detailed Performance Report: DeepSeek-R1

**Model ID:** `deepseek-r1`  
**Provider:** Deepseek  
**Parameters:** 671B (37B active, MoE)  
**Context Window:** 128,000 tokens  

---

## 1. Executive Summary

This report details the benchmarking performance of **DeepSeek-R1** across 7 distinct task categories. 
The model achieved a general accuracy score of **94.4/100**, demonstrating its capabilities in this specific configuration tier.

---

## 2. Capability Matrix

| Feature | Supported |
| :--- | :---: |
| **Vision (Multimodal)** | ❌ |
| **Audio (Multimodal)** | ❌ |
| **Function Calling / Tools** | ❌ |
| **Native JSON Mode** | ❌ |
| **Chain-of-Thought Reasoning** | ✅ |

---

## 3. Benchmarking Performance Metrics

### A. Intelligence & Accuracy
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **General Accuracy (EM)** | **94.4%** | Overall factual correctness on zero-shot prompts. |
| **F1 Score** | **0.946** | Semantic overlap with reference answers. |
| **Code Generation** | **93.1%** | Performance on algorithmic and debugging tasks. |
| **Indian Languages** | **98.5%** | Performance on translation and native Indic queries. |

### B. Speed & Latency
| Metric | Value | Analysis |
| :--- | :--- | :--- |
| **Time To First Token (TTFT)** | **2.407 s** | The responsiveness of the model to begin generating. |
| **Total Turnaround Time** | **3.90 s** | Average time to complete a full response. |

### C. Safety & Robustness
| Metric | Score | Analysis |
| :--- | :--- | :--- |
| **Safety & Robustness Rate** | **88.6%** | Resistance to jailbreaks, hallucinations, and injection attacks. |

### D. Cost Economics
*Based on simulated benchmark runs mixing input and output tokens.*
| Metric | Value |
| :--- | :--- |
| **Estimated Cost** | **$18.12** |

---

## 4. Strengths and Weaknesses

**Key Strengths:**
* Highly efficient execution speed.
* Strong native reasoning capabilities due to integrated Chain-of-Thought.
* Reliable deep processing capabilities.

**Known Limitations:**
* No function calling or JSON mode
* Verbose reasoning traces

---
*Report generated automatically by the LLM Benchmarking Framework.*
