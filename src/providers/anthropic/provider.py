"""Anthropic Claude provider adapter — Claude Opus 4, Sonnet 4, Haiku 3.5."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class AnthropicProvider(LLMProvider):
    """Adapter for Anthropic Claude models."""

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set.")

        self.client = anthropic.Anthropic(api_key=api_key)
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
        kwargs = {
            "model": self.api_model_id,
            "max_tokens": opts.get("max_tokens", 1024),
            "temperature": opts.get("temperature", 0.0),
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""
        input_tokens = 0
        output_tokens = 0

        try:
            with self.client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += text

            # Get usage from final message
            final = stream.get_final_message()
            input_tokens = final.usage.input_tokens
            output_tokens = final.usage.output_tokens

            total_time = time.perf_counter() - start_time
            ttft = (first_token_time - start_time) if first_token_time else total_time
            tps = output_tokens / max(total_time - ttft, 0.001)

            return LLMResponse(
                prediction=full_text.strip(),
                model=self.model_id,
                provider="anthropic",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4),
                total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=self.calculate_cost(input_tokens, output_tokens),
            )
        except Exception as e:
            logger.error(f"[Anthropic] Error for {self.model_id}: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="anthropic",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(self, prompt, system_prompt=None, options=None) -> Iterator[str]:
        opts = options or {}
        kwargs = {
            "model": self.api_model_id,
            "max_tokens": opts.get("max_tokens", 1024),
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=self.config.get("multimodal", {}).get("vision", False),
            streaming=True,
            function_calling=self.config.get("function_calling", False),
            json_mode=self.config.get("json_mode", False),
            reasoning_cot=self.config.get("reasoning_cot", False),
            code_generation=True,
            multilingual=True,
            max_context_window=self.config.get("context_window", 200000),
            max_output_tokens=self.config.get("max_output_tokens", 4096),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
