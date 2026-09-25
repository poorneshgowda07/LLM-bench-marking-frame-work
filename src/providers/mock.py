"""Mock LLM provider for testing without API keys."""
import time
import random
import hashlib
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix


# Deterministic mock responses keyed by prompt hash prefix
MOCK_RESPONSES = {
    "factual_qa": "The answer is: {answer}. This is a mock response for testing.",
    "code": "```python\ndef mock_solution():\n    # Mock implementation\n    return 'result'\n```",
    "translation": "[MOCK TRANSLATION] यह एक परीक्षण अनुवाद है।",
    "summary": "This is a mock summary of the provided text. Key points have been extracted.",
    "json": '{"result": "mock", "confidence": 0.95}',
    "default": "This is a deterministic mock response for testing the LLM benchmarking pipeline. No API key required.",
}


class MockProvider(LLMProvider):
    """Mock provider that returns deterministic responses for pipeline testing.

    Useful for:
    - CI/CD validation
    - Testing metrics without API costs
    - End-to-end pipeline verification
    """

    def __init__(self, model_id: str = "mock", config: Dict[str, Any] = None):
        super().__init__(model_id=model_id, config=config or {})
        self.provider_name = "mock"
        # Simulated latency settings
        self._ttft_range = (0.05, 0.15)  # seconds
        self._tps_range = (50, 150)  # tokens per second

    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        opts = options or {}
        max_tokens = opts.get("max_tokens", 256)

        # Deterministic response based on prompt content
        response_text = self._generate_mock_response(prompt)

        # Simulate realistic latency
        ttft = random.uniform(*self._ttft_range)
        words = response_text.split()
        output_tokens = len(words)
        tps = random.uniform(*self._tps_range)
        generation_time = output_tokens / tps
        total_time = ttft + generation_time

        time.sleep(min(total_time, 0.5))  # Cap sleep at 0.5s for speed

        input_tokens = len(prompt.split())
        timestamp = datetime.now(timezone.utc).isoformat()

        return LLMResponse(
            prediction=response_text,
            model=self.model_id,
            provider="mock",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            ttft=ttft,
            total_time=total_time,
            tokens_per_second=tps,
            timestamp=timestamp,
            cost_usd=0.0,
        )

    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        response = self._generate_mock_response(prompt)
        words = response.split()
        time.sleep(random.uniform(*self._ttft_range))  # simulate TTFT
        for word in words:
            yield word + " "
            time.sleep(0.02)  # simulate token streaming

    def _generate_mock_response(self, prompt: str) -> str:
        """Generate a deterministic mock response based on prompt keywords."""
        prompt_lower = prompt.lower()
        if any(kw in prompt_lower for kw in ["capital", "who", "what is", "when", "where"]):
            return "Mock factual answer: The answer to your question is a well-known fact. This is a deterministic mock response."
        elif any(kw in prompt_lower for kw in ["def ", "function", "python", "code", "sql", "javascript"]):
            return "```python\ndef mock_function(input_data):\n    \"\"\"Mock implementation for testing.\"\"\"\n    result = process(input_data)\n    return result\n```\nThis is a mock code response."
        elif any(kw in prompt_lower for kw in ["hindi", "translate", "kannada", "tamil", "hinglish"]):
            return "यह एक परीक्षण अनुवाद है। This is a mock translation response for Indian language testing."
        elif any(kw in prompt_lower for kw in ["summarize", "summary", "extract"]):
            return "Mock summary: The provided text discusses key topics that are summarized here for testing purposes. Three main points were identified."
        elif any(kw in prompt_lower for kw in ["synthesize", "hack", "phishing", "bleach", "illegal"]):
            return "I'm sorry, but I can't help with that request as it may be harmful or illegal. Please ask me something else."
        elif "json" in prompt_lower or "{" in prompt:
            return '{"mock_result": "test_value", "confidence": 0.95, "status": "success"}'
        else:
            hash_prefix = hashlib.md5(prompt.encode()).hexdigest()[:8]
            return f"Mock response [{hash_prefix}]: This is a deterministic test response for the LLM benchmarking pipeline. The pipeline is working correctly without any API keys required."

    def get_capabilities(self) -> CapabilityMatrix:
        return CapabilityMatrix(
            vision=True, audio=True, streaming=True,
            function_calling=True, json_mode=True,
            reasoning_cot=True, code_generation=True,
            multilingual=True, fine_tuning=False,
            max_context_window=999999, max_output_tokens=4096,
            pricing_input_per_1m=0.0, pricing_output_per_1m=0.0,
        )
