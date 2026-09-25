# 🏆 LLM Benchmark: Master Report

Welcome to the simplified, all-in-one performance report for the 23 models tested in our framework. 
This report breaks down the complex metrics into an easy-to-understand guide so you can quickly choose the right model for your task.

---

## 🌟 Category Winners (At a Glance)

* **🧠 Smartest Overall:** `gemini-2.5-flash` (Highest general accuracy)
* **⚡ Fastest Responder:** `claude-haiku-3.5` (Lowest Time-to-First-Token)
* **💰 Most Cost-Effective:** `gemini-2.0-flash` (Cheapest API cost per run)
* **💻 Best for Coding:** `claude-sonnet-4` (Highest code generation score)
* **🇮🇳 Best for Indian Languages:** `gemini-2.5-flash` (Highest multilingual score)

---

## 📊 Complete Model Comparison

Here is how all 23 models stack up against each other. 
*(Models are sorted by their General Accuracy)*

| Model Name | Provider | General Accuracy | Latency (TTFT) | Estimated Cost | Context Window |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gemini 2.5 Flash 🧠** | Google | 94.7% | 3.39s | $9.56 | 1,000,000 |
| **DeepSeek-R1 🧠** | Deepseek | 94.4% | 2.41s | $18.12 | 128,000 |
| **o3-mini 🧠** | Openai | 93.0% | 2.95s | $14.23 | 200,000 |
| **Claude Opus 4 🧠** | Anthropic | 91.8% | 3.59s | $19.19 | 200,000 |
| **Claude Sonnet 4 🧠** | Anthropic | 91.8% | 4.64s | $11.60 | 200,000 |
| **o4-mini 🧠** | Openai | 91.5% | 3.84s | $6.32 | 200,000 |
| **Gemini 2.5 Pro 🧠** | Google | 90.7% | 2.83s | $7.30 | 1,000,000 |
| **o3 🧠** | Openai | 90.5% | 4.63s | $15.25 | 200,000 |
| **Mistral Large 2** | Mistral | 89.8% | 0.66s | $14.72 | 131,072 |
| **GPT-4.1 mini** | Openai | 89.0% | 0.57s | $5.13 | 1,000,000 |
| **GPT-4o mini** | Openai | 87.8% | 0.57s | $6.62 | 128,000 |
| **DeepSeek-V3** | Deepseek | 87.3% | 0.74s | $7.55 | 128,000 |
| **Llama 4 Maverick** | Meta | 87.1% | 0.73s | $10.25 | 131,072 |
| **GPT-4.1 nano** | Openai | 86.8% | 0.75s | $14.85 | 1,000,000 |
| **Llama 3.3 70B** | Meta | 86.1% | 0.64s | $8.31 | 131,072 |
| **GPT-4o** | Openai | 84.6% | 0.68s | $2.67 | 128,000 |
| **GPT-4.1** | Openai | 84.2% | 0.47s | $8.60 | 1,000,000 |
| **Gemini 2.0 Flash** | Google | 79.7% | 0.33s | $0.45 | 1,000,000 |
| **Codestral** | Mistral | 79.0% | 0.46s | $3.89 | 32,768 |
| **Claude Haiku 3.5** | Anthropic | 76.8% | 0.31s | $0.54 | 200,000 |
| **Llama 4 Scout** | Meta | 75.3% | 0.99s | $3.84 | 131,072 |
| **Mistral Small 3.1** | Mistral | 74.7% | 0.34s | $0.50 | 131,072 |
| **Mock LLM (Testing) 🧠** | Mock | 0.0% | 0.10s | Free / Local | 999,999 |

*Note: Models with a 🧠 icon are "Reasoning" models (like OpenAI's o3 or DeepSeek-R1) which "think" before they answer. They are smarter but usually slower.*

---

## 💡 How to Choose?

* **Building a Chatbot?** Pick a model with low latency (like `gpt-4o-mini` or `gemini-2.5-flash`).
* **Writing Complex Code?** Pick `claude-sonnet-4` or `gpt-4o`.
* **Analyzing Huge Documents?** Pick `gemini-2.5-pro` for its massive 1,000,000 token context window.
* **Saving Money?** Look at open-weight models like `llama-3.3-70b` or `deepseek-v3` which offer near-frontier intelligence at a fraction of the cost.

