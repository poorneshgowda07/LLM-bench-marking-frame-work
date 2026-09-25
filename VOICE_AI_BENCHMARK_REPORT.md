# 🎙️ Comprehensive LLM Benchmarking Report: Focus on Voice AI Agents

This extensive report provides an in-depth, individual analysis of all 23 models tested in the framework. 
It concludes with a holistic comparison and a specialized recommendation engine for building **Voice AI Agents** (where latency, empathy, and cost are critical).

---

## 📖 PART 1: Detailed Individual Model Profiles

### Gemini 2.5 Flash (`gemini-2.5-flash`)
**Provider:** Google | **Context Window:** 1,000,000 tokens | **Parameters:** ~30B

**Capabilities:** 👁️ Vision, 🎧 Native Audio, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 94.7% (F1: 0.933)
- **Code Generation:** 93.5%
- **Indian Languages:** 98.6%
- **Latency (TTFT):** 3.39s
- **Estimated Cost per 1M Tokens:** $9.56

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* No major structural limitations noted for its class.
---

### DeepSeek-R1 (`deepseek-r1`)
**Provider:** Deepseek | **Context Window:** 128,000 tokens | **Parameters:** 671B (37B active, MoE)

**Capabilities:** 🧠 Reasoning (CoT)

**Performance Metrics:**
- **Accuracy:** 94.4% (F1: 0.946)
- **Code Generation:** 93.1%
- **Indian Languages:** 98.5%
- **Latency (TTFT):** 2.41s
- **Estimated Cost per 1M Tokens:** $18.12

**Strengths:**
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* No function calling or JSON mode
* Verbose reasoning traces
---

### o3-mini (`o3-mini`)
**Provider:** Openai | **Context Window:** 200,000 tokens | **Parameters:** ~20B

**Capabilities:** 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 93.0% (F1: 0.950)
- **Code Generation:** 91.8%
- **Indian Languages:** 97.4%
- **Latency (TTFT):** 2.95s
- **Estimated Cost per 1M Tokens:** $14.23

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* No vision input
---

### Claude Opus 4 (`claude-opus-4`)
**Provider:** Anthropic | **Context Window:** 200,000 tokens | **Parameters:** ~500B

**Capabilities:** 👁️ Vision, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 91.8% (F1: 0.908)
- **Code Generation:** 94.0%
- **Indian Languages:** 93.3%
- **Latency (TTFT):** 3.59s
- **Estimated Cost per 1M Tokens:** $19.19

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* Most expensive model in suite
* No audio input
---

### Claude Sonnet 4 (`claude-sonnet-4`)
**Provider:** Anthropic | **Context Window:** 200,000 tokens | **Parameters:** ~100B

**Capabilities:** 👁️ Vision, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 91.8% (F1: 0.933)
- **Code Generation:** 96.7%
- **Indian Languages:** 89.2%
- **Latency (TTFT):** 4.64s
- **Estimated Cost per 1M Tokens:** $11.60

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* No audio input
---

### o4-mini (`o4-mini`)
**Provider:** Openai | **Context Window:** 200,000 tokens | **Parameters:** ~30B

**Capabilities:** 👁️ Vision, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 91.5% (F1: 0.935)
- **Code Generation:** 93.9%
- **Indian Languages:** 82.2%
- **Latency (TTFT):** 3.84s
- **Estimated Cost per 1M Tokens:** $6.32

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* No major structural limitations noted for its class.
---

### Gemini 2.5 Pro (`gemini-2.5-pro`)
**Provider:** Google | **Context Window:** 1,000,000 tokens | **Parameters:** ~1T (MoE)

**Capabilities:** 👁️ Vision, 🎧 Native Audio, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 90.7% (F1: 0.904)
- **Code Generation:** 95.0%
- **Indian Languages:** 97.6%
- **Latency (TTFT):** 2.83s
- **Estimated Cost per 1M Tokens:** $7.30

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* Rate limits on free tier
---

### o3 (`o3`)
**Provider:** Openai | **Context Window:** 200,000 tokens | **Parameters:** ~200B

**Capabilities:** 👁️ Vision, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 90.5% (F1: 0.917)
- **Code Generation:** 87.6%
- **Indian Languages:** 84.4%
- **Latency (TTFT):** 4.63s
- **Estimated Cost per 1M Tokens:** $15.25

**Strengths:**
* Massive context window for large document processing.
* Frontier-level intelligence and deep reasoning capabilities.
**Limitations:**
* Slower due to extended thinking
* Higher cost
---

### Mistral Large 2 (`mistral-large`)
**Provider:** Mistral | **Context Window:** 131,072 tokens | **Parameters:** 123B

**Capabilities:** ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 89.8% (F1: 0.886)
- **Code Generation:** 84.9%
- **Indian Languages:** 91.0%
- **Latency (TTFT):** 0.66s
- **Estimated Cost per 1M Tokens:** $14.72

**Strengths:**
**Limitations:**
* No vision/audio
---

### GPT-4.1 mini (`gpt-4.1-mini`)
**Provider:** Openai | **Context Window:** 1,000,000 tokens | **Parameters:** ~20B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 89.0% (F1: 0.876)
- **Code Generation:** 91.6%
- **Indian Languages:** 84.1%
- **Latency (TTFT):** 0.57s
- **Estimated Cost per 1M Tokens:** $5.13

**Strengths:**
* Massive context window for large document processing.
**Limitations:**
* No major structural limitations noted for its class.
---

### GPT-4o mini (`gpt-4o-mini`)
**Provider:** Openai | **Context Window:** 128,000 tokens | **Parameters:** ~8B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 87.8% (F1: 0.878)
- **Code Generation:** 90.9%
- **Indian Languages:** 80.1%
- **Latency (TTFT):** 0.57s
- **Estimated Cost per 1M Tokens:** $6.62

**Strengths:**
**Limitations:**
* Smaller context understanding vs GPT-4o
---

### DeepSeek-V3 (`deepseek-v3`)
**Provider:** Deepseek | **Context Window:** 128,000 tokens | **Parameters:** 671B (37B active, MoE)

**Capabilities:** ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 87.3% (F1: 0.867)
- **Code Generation:** 88.5%
- **Indian Languages:** 91.2%
- **Latency (TTFT):** 0.74s
- **Estimated Cost per 1M Tokens:** $7.55

**Strengths:**
**Limitations:**
* No vision/audio
* API may have latency from Chinese servers
---

### Llama 4 Maverick (`llama-4-maverick`)
**Provider:** Meta | **Context Window:** 131,072 tokens | **Parameters:** 400B (17B active, MoE)

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 87.1% (F1: 0.891)
- **Code Generation:** 88.2%
- **Indian Languages:** 84.9%
- **Latency (TTFT):** 0.73s
- **Estimated Cost per 1M Tokens:** $10.25

**Strengths:**
**Limitations:**
* Requires Together AI or local Ollama
---

### GPT-4.1 nano (`gpt-4.1-nano`)
**Provider:** Openai | **Context Window:** 1,000,000 tokens | **Parameters:** ~4B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 86.8% (F1: 0.865)
- **Code Generation:** 82.7%
- **Indian Languages:** 83.3%
- **Latency (TTFT):** 0.75s
- **Estimated Cost per 1M Tokens:** $14.85

**Strengths:**
* Massive context window for large document processing.
**Limitations:**
* Lower accuracy on complex tasks
---

### Llama 3.3 70B (`llama-3.3-70b`)
**Provider:** Meta | **Context Window:** 131,072 tokens | **Parameters:** 70B

**Capabilities:** ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 86.1% (F1: 0.842)
- **Code Generation:** 84.7%
- **Indian Languages:** 89.5%
- **Latency (TTFT):** 0.64s
- **Estimated Cost per 1M Tokens:** $8.31

**Strengths:**
**Limitations:**
* No vision/audio
---

### GPT-4o (`gpt-4o`)
**Provider:** Openai | **Context Window:** 128,000 tokens | **Parameters:** ~200B

**Capabilities:** 👁️ Vision, 🎧 Native Audio, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 84.6% (F1: 0.847)
- **Code Generation:** 80.4%
- **Indian Languages:** 83.8%
- **Latency (TTFT):** 0.68s
- **Estimated Cost per 1M Tokens:** $2.67

**Strengths:**
**Limitations:**
* Knowledge cutoff April 2024
* No real-time internet access
---

### GPT-4.1 (`gpt-4.1`)
**Provider:** Openai | **Context Window:** 1,000,000 tokens | **Parameters:** ~200B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 84.2% (F1: 0.844)
- **Code Generation:** 82.3%
- **Indian Languages:** 75.1%
- **Latency (TTFT):** 0.47s
- **Estimated Cost per 1M Tokens:** $8.60

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
* Massive context window for large document processing.
**Limitations:**
* Knowledge cutoff June 2025
---

### Gemini 2.0 Flash (`gemini-2.0-flash`)
**Provider:** Google | **Context Window:** 1,000,000 tokens | **Parameters:** ~20B

**Capabilities:** 👁️ Vision, 🎧 Native Audio, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 79.7% (F1: 0.795)
- **Code Generation:** 82.8%
- **Indian Languages:** 84.3%
- **Latency (TTFT):** 0.33s
- **Estimated Cost per 1M Tokens:** $0.45

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
* Massive context window for large document processing.
**Limitations:**
* Smaller output window vs 2.5
---

### Codestral (`codestral`)
**Provider:** Mistral | **Context Window:** 32,768 tokens | **Parameters:** 22B

**Capabilities:** Text Only

**Performance Metrics:**
- **Accuracy:** 79.0% (F1: 0.800)
- **Code Generation:** 74.2%
- **Indian Languages:** 73.4%
- **Latency (TTFT):** 0.46s
- **Estimated Cost per 1M Tokens:** $3.89

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
**Limitations:**
* Code-only, not suitable for general tasks
* No function calling or JSON mode
---

### Claude Haiku 3.5 (`claude-haiku-3.5`)
**Provider:** Anthropic | **Context Window:** 200,000 tokens | **Parameters:** ~20B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 76.8% (F1: 0.771)
- **Code Generation:** 80.7%
- **Indian Languages:** 80.4%
- **Latency (TTFT):** 0.31s
- **Estimated Cost per 1M Tokens:** $0.54

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
* Massive context window for large document processing.
**Limitations:**
* Lower reasoning depth
---

### Llama 4 Scout (`llama-4-scout`)
**Provider:** Meta | **Context Window:** 131,072 tokens | **Parameters:** 109B (17B active, MoE)

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 75.3% (F1: 0.752)
- **Code Generation:** 75.7%
- **Indian Languages:** 66.2%
- **Latency (TTFT):** 0.99s
- **Estimated Cost per 1M Tokens:** $3.84

**Strengths:**
**Limitations:**
* Requires Together AI or local Ollama for API access
---

### Mistral Small 3.1 (`mistral-small`)
**Provider:** Mistral | **Context Window:** 131,072 tokens | **Parameters:** 24B

**Capabilities:** 👁️ Vision, ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 74.7% (F1: 0.747)
- **Code Generation:** 76.9%
- **Indian Languages:** 68.7%
- **Latency (TTFT):** 0.34s
- **Estimated Cost per 1M Tokens:** $0.50

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
**Limitations:**
* No major structural limitations noted for its class.
---

### Mock LLM (Testing) (`mock`)
**Provider:** Mock | **Context Window:** 999,999 tokens | **Parameters:** N/A

**Capabilities:** 👁️ Vision, 🎧 Native Audio, 🧠 Reasoning (CoT), ⚙️ JSON Mode

**Performance Metrics:**
- **Accuracy:** 0.0% (F1: 0.000)
- **Code Generation:** 0.3%
- **Indian Languages:** 0.0%
- **Latency (TTFT):** 0.10s
- **Estimated Cost per 1M Tokens:** Free / Local

**Strengths:**
* Ultra-low latency, excellent for real-time applications.
* Massive context window for large document processing.
**Limitations:**
* Returns deterministic mock responses
* Not suitable for real evaluation
---

## 📊 PART 2: Overall Model Comparison

*(Models sorted by General Accuracy)*

| Model Name | Provider | Accuracy | TTFT (s) | Cost ($) | Audio Input |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 2.5 Flash 🧠** | Google | 94.7% | 3.39s | $9.56 | ✅ |
| **DeepSeek-R1 🧠** | Deepseek | 94.4% | 2.41s | $18.12 | ❌ |
| **o3-mini 🧠** | Openai | 93.0% | 2.95s | $14.23 | ❌ |
| **Claude Opus 4 🧠** | Anthropic | 91.8% | 3.59s | $19.19 | ❌ |
| **Claude Sonnet 4 🧠** | Anthropic | 91.8% | 4.64s | $11.60 | ❌ |
| **o4-mini 🧠** | Openai | 91.5% | 3.84s | $6.32 | ❌ |
| **Gemini 2.5 Pro 🧠** | Google | 90.7% | 2.83s | $7.30 | ✅ |
| **o3 🧠** | Openai | 90.5% | 4.63s | $15.25 | ❌ |
| **Mistral Large 2** | Mistral | 89.8% | 0.66s | $14.72 | ❌ |
| **GPT-4.1 mini** | Openai | 89.0% | 0.57s | $5.13 | ❌ |
| **GPT-4o mini** | Openai | 87.8% | 0.57s | $6.62 | ❌ |
| **DeepSeek-V3** | Deepseek | 87.3% | 0.74s | $7.55 | ❌ |
| **Llama 4 Maverick** | Meta | 87.1% | 0.73s | $10.25 | ❌ |
| **GPT-4.1 nano** | Openai | 86.8% | 0.75s | $14.85 | ❌ |
| **Llama 3.3 70B** | Meta | 86.1% | 0.64s | $8.31 | ❌ |
| **GPT-4o** | Openai | 84.6% | 0.68s | $2.67 | ✅ |
| **GPT-4.1** | Openai | 84.2% | 0.47s | $8.60 | ❌ |
| **Gemini 2.0 Flash** | Google | 79.7% | 0.33s | $0.45 | ✅ |
| **Codestral** | Mistral | 79.0% | 0.46s | $3.89 | ❌ |
| **Claude Haiku 3.5** | Anthropic | 76.8% | 0.31s | $0.54 | ❌ |
| **Llama 4 Scout** | Meta | 75.3% | 0.99s | $3.84 | ❌ |
| **Mistral Small 3.1** | Mistral | 74.7% | 0.34s | $0.50 | ❌ |
| **Mock LLM (Testing) 🧠** | Mock | 0.0% | 0.10s | Free | ✅ |

---

## 🎧 PART 3: The Ultimate Guide for Voice AI Agents

When building Voice AI Agents (like customer service bots, virtual companions, or telephony agents), traditional metrics like Coding Accuracy don't matter as much. **The three pillars of Voice AI are:**

1. **Latency (TTFT):** Humans expect a response within 500-700ms in a conversation. Any TTFT > 1.0s breaks the illusion of a natural conversation.
2. **Cost Efficiency:** Voice bots generate thousands of short tokens continuously. High-cost models burn budget rapidly.
3. **Conversational Formatting (Empathy & Brevity):** The model must follow instructions to keep answers short, empathetic, and free of unpronounceable characters (like markdown `**bold**` asterisks).

### 🏆 Top Recommendations for Voice AI

#### 🥇 1. The Overall Winner: `gemini-2.0-flash` or `claude-haiku-3.5`
For text-in/text-out voice pipelines (ASR -> LLM -> TTS), **Claude Haiku 3.5** and **Gemini 2.0 Flash** are the absolute best choices. 
* **Why?** They both consistently hit a Time-To-First-Token (TTFT) of **< 0.35 seconds**. They are aggressively cheap (Under $0.60 per 1M tokens), and highly steerable for conversational empathy.

#### 🥈 2. The Native Audio Winner: `gpt-4o` & `gemini-2.5-flash`
If you are bypassing traditional ASR/TTS and using **Native Audio-in / Audio-out** (Speech-to-Speech), you must use a model that natively supports the `audio` modality.
* **Why?** GPT-4o and Gemini 2.5 natively understand audio tone, emotion, and background noise, and can output native audio with inflections that text-to-speech engines struggle to mimic. GPT-4o maintains a TTFT of ~0.68s even on complex voice interactions.

#### 🥉 3. The Open-Weight / Local Winner: `llama-3.3-70b`
If you are deploying on your own hardware for data privacy (e.g., healthcare Voice AI), **Llama 3.3 70B** is the best option.
* **Why?** Hosted via fast inference engines like vLLM or Together AI, it achieves ~0.64s TTFT. While it lacks native audio, its conversational logic is on par with GPT-4, and it can be run entirely in a HIPAA-compliant local cloud.

### 🚫 Models to AVOID for Voice AI
* **Reasoning Models (o3, DeepSeek-R1, Claude Opus):** Do not use these for Voice AI. Their architecture requires "thinking" time, pushing their TTFT to 2.5s - 4.5s. This causes massive, awkward silences on a phone call.
