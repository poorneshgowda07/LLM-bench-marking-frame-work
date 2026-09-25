"""OpenAI provider adapter supporting GPT-4o, GPT-4.1, o3/o4 families."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class OpenAIProvider(LLMProvider):
    """Adapter for OpenAI models: GPT-4o, GPT-4.1, o3, o4-mini, etc.

    Supports both standard completions and streaming.
    Reasoning models (o3, o4-mini) use reasoning_effort parameter.
    """

    # Models that use the 'reasoning' API (no temperature, use reasoning_effort)
    REASONING_MODELS = {"o3", "o3-mini", "o4-mini", "o1", "o1-mini"}

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not set in environment.")

        base_url = config.get("base_url", "https://api.openai.com/v1")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.api_model_id = config.get("api_model_id", model_id)
        self._pricing = config.get("pricing", {"input_per_1m": 0, "output_per_1m": 0})
        self._is_reasoning = any(rm in self.api_model_id for rm in self.REASONING_MODELS)

    @retry_with_backoff(max_retries=3, backoff_factor=2.0)
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        opts = options or {}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.api_model_id,
            "messages": messages,
            "max_completion_tokens": opts.get("max_tokens", 1024),
            "stream": True,  # Always stream to measure TTFT
        }

        # Reasoning models don't support temperature
        if not self._is_reasoning:
            kwargs["temperature"] = opts.get("temperature", 0.0)
            kwargs["top_p"] = opts.get("top_p", 1.0)

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""
        input_tokens = 0
        output_tokens = 0

        try:
            stream = self.client.chat.completions.create(**kwargs)
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += chunk.choices[0].delta.content
                # Capture usage if available
                if hasattr(chunk, "usage") and chunk.usage:
                    input_tokens = chunk.usage.prompt_tokens or 0
                    output_tokens = chunk.usage.completion_tokens or 0

            total_time = time.perf_counter() - start_time
            ttft = (first_token_time - start_time) if first_token_time else total_time

            # Estimate tokens if not returned
            if output_tokens == 0:
                output_tokens = max(1, len(full_text.split()))
            if input_tokens == 0:
                input_tokens = max(1, len(prompt.split()))

            tps = output_tokens / max(total_time - ttft, 0.001)
            cost = self.calculate_cost(input_tokens, output_tokens)

            return LLMResponse(
                prediction=full_text.strip(),
                model=self.model_id,
                provider="openai",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4),
                total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=cost,
            )
        except Exception as e:
            logger.error(f"[OpenAI] Error for model {self.model_id}: {e}")
            return LLMResponse(
                prediction="",
                model=self.model_id,
                provider="openai",
                error=str(e),
                is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        opts = options or {}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.api_model_id,
            "messages": messages,
            "stream": True,
            "max_completion_tokens": opts.get("max_tokens", 1024),
        }
        if not self._is_reasoning:
            kwargs["temperature"] = opts.get("temperature", 0.0)

        stream = self.client.chat.completions.create(**kwargs)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=self.config.get("multimodal", {}).get("vision", False),
            audio=self.config.get("multimodal", {}).get("audio", False),
            streaming=True,
            function_calling=self.config.get("function_calling", False),
            json_mode=self.config.get("json_mode", False),
            reasoning_cot=self._is_reasoning,
            code_generation=True,
            multilingual=True,
            max_context_window=self.config.get("context_window", 128000),
            max_output_tokens=self.config.get("max_output_tokens", 4096),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
