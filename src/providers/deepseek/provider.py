"""DeepSeek provider adapter — DeepSeek-V3 and DeepSeek-R1."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

try:
    from openai import OpenAI  # DeepSeek uses OpenAI-compatible API
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class DeepSeekProvider(LLMProvider):
    """Adapter for DeepSeek models using their OpenAI-compatible API.

    DeepSeek-R1 is a reasoning model with extended thinking chains.
    DeepSeek-V3 is a general-purpose MoE model.
    """

    REASONING_MODELS = {"deepseek-r1", "deepseek-reasoner"}

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        if not DEEPSEEK_AVAILABLE:
            raise ImportError("openai package required for DeepSeek. Run: pip install openai")

        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise EnvironmentError("DEEPSEEK_API_KEY not set.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=config.get("base_url", "https://api.deepseek.com/v1"),
        )
        self.api_model_id = config.get("api_model_id", model_id)
        self._pricing = config.get("pricing", {"input_per_1m": 0, "output_per_1m": 0})
        self._is_reasoning = self.api_model_id in self.REASONING_MODELS or "r1" in model_id

    @retry_with_backoff(max_retries=3, backoff_factor=2.0)
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        opts = options or {}
        messages = []
        if system_prompt and not self._is_reasoning:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.api_model_id,
            "messages": messages,
            "max_tokens": opts.get("max_tokens", 1024),
            "stream": True,
        }
        if not self._is_reasoning:
            kwargs["temperature"] = opts.get("temperature", 0.0)

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""
        reasoning_text = ""  # R1 has reasoning_content field
        input_tokens = 0
        output_tokens = 0

        try:
            stream = self.client.chat.completions.create(**kwargs)
            for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    # R1 may have reasoning_content
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                        reasoning_text += delta.reasoning_content
                    if delta.content:
                        if first_token_time is None:
                            first_token_time = time.perf_counter()
                        full_text += delta.content
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
                prediction=full_text.strip(),
                model=self.model_id, provider="deepseek",
                input_tokens=input_tokens, output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4), total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=self.calculate_cost(input_tokens, output_tokens),
                raw_response={"reasoning": reasoning_text} if reasoning_text else {},
            )
        except Exception as e:
            logger.error(f"[DeepSeek] Error for {self.model_id}: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="deepseek",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(self, prompt, system_prompt=None, options=None) -> Iterator[str]:
        response = self.complete(prompt, system_prompt, options)
        yield response.prediction

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=False, audio=False, streaming=True,
            function_calling=not self._is_reasoning,
            json_mode=not self._is_reasoning,
            reasoning_cot=self._is_reasoning,
            code_generation=True, multilingual=True,
            max_context_window=self.config.get("context_window", 128000),
            max_output_tokens=self.config.get("max_output_tokens", 8192),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
