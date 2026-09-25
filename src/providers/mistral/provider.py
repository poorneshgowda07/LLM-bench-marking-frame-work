"""Mistral AI provider adapter — Mistral Large, Small, Codestral."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

try:
    from openai import OpenAI  # Mistral uses OpenAI-compatible API
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class MistralProvider(LLMProvider):
    """Adapter for Mistral AI models via the Mistral API.

    Uses the OpenAI-compatible endpoint (api.mistral.ai/v1).
    Codestral has a separate endpoint for FIM (Fill-in-Middle) tasks.
    """

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        if not MISTRAL_AVAILABLE:
            raise ImportError("openai package required. Run: pip install openai")

        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise EnvironmentError("MISTRAL_API_KEY not set.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=config.get("base_url", "https://api.mistral.ai/v1"),
        )
        self.api_model_id = config.get("api_model_id", model_id)
        self._pricing = config.get("pricing", {"input_per_1m": 0, "output_per_1m": 0})

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

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""
        input_tokens = 0
        output_tokens = 0

        try:
            stream = self.client.chat.completions.create(
                model=self.api_model_id,
                messages=messages,
                max_tokens=opts.get("max_tokens", 1024),
                temperature=opts.get("temperature", 0.0),
                stream=True,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += chunk.choices[0].delta.content
                if hasattr(chunk, "usage") and chunk.usage:
                    input_tokens = chunk.usage.prompt_tokens or 0
                    output_tokens = chunk.usage.completion_tokens or 0

            total_time = time.perf_counter() - start_time
            ttft = (first_token_time - start_time) if first_token_time else total_time
            if output_tokens == 0:
                output_tokens = len(full_text.split())
            if input_tokens == 0:
                input_tokens = len(prompt.split())
            tps = output_tokens / max(total_time - ttft, 0.001)

            return LLMResponse(
                prediction=full_text.strip(), model=self.model_id, provider="mistral",
                input_tokens=input_tokens, output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4), total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=self.calculate_cost(input_tokens, output_tokens),
            )
        except Exception as e:
            logger.error(f"[Mistral] Error for {self.model_id}: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="mistral",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(self, prompt, system_prompt=None, options=None) -> Iterator[str]:
        opts = options or {}
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        stream = self.client.chat.completions.create(
            model=self.api_model_id, messages=messages,
            max_tokens=opts.get("max_tokens", 1024), stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=self.config.get("multimodal", {}).get("vision", False),
            streaming=True,
            function_calling=self.config.get("function_calling", False),
            json_mode=self.config.get("json_mode", False),
            code_generation=True,
            multilingual=self.config.get("multilingual", True),
            max_context_window=self.config.get("context_window", 131072),
            max_output_tokens=self.config.get("max_output_tokens", 8192),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
