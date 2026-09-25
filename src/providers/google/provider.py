"""Google Gemini provider adapter — Gemini 2.5 Pro/Flash, 2.0 Flash."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class GoogleProvider(LLMProvider):
    """Adapter for Google Gemini models via the Google AI Studio API."""

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        if not GOOGLE_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")

        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set.")

        genai.configure(api_key=api_key)
        self.api_model_id = config.get("api_model_id", model_id)
        self._model = genai.GenerativeModel(self.api_model_id)
        self._pricing = config.get("pricing", {"input_per_1m": 0, "output_per_1m": 0})

    @retry_with_backoff(max_retries=3, backoff_factor=2.0)
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        opts = options or {}
        generation_config = genai.types.GenerationConfig(
            temperature=opts.get("temperature", 0.0),
            max_output_tokens=opts.get("max_tokens", 1024),
            top_p=opts.get("top_p", 1.0),
        )

        # Build prompt with optional system context
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""
        input_tokens = 0
        output_tokens = 0

        try:
            # Use streaming to capture TTFT
            stream = self._model.generate_content(
                full_prompt,
                generation_config=generation_config,
                stream=True,
            )

            for chunk in stream:
                if chunk.text:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += chunk.text

            # Get usage metadata from the stream
            try:
                usage = stream.usage_metadata
                input_tokens = usage.prompt_token_count or len(prompt.split())
                output_tokens = usage.candidates_token_count or len(full_text.split())
            except Exception:
                input_tokens = len(prompt.split())
                output_tokens = len(full_text.split())

            total_time = time.perf_counter() - start_time
            ttft = (first_token_time - start_time) if first_token_time else total_time
            tps = output_tokens / max(total_time - ttft, 0.001)

            return LLMResponse(
                prediction=full_text.strip(),
                model=self.model_id,
                provider="google",
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
            logger.error(f"[Google] Error for {self.model_id}: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="google",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(self, prompt, system_prompt=None, options=None) -> Iterator[str]:
        opts = options or {}
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        config = genai.types.GenerationConfig(
            temperature=opts.get("temperature", 0.0),
            max_output_tokens=opts.get("max_tokens", 1024),
        )
        stream = self._model.generate_content(full_prompt, generation_config=config, stream=True)
        for chunk in stream:
            if chunk.text:
                yield chunk.text

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=self.config.get("multimodal", {}).get("vision", False),
            audio=self.config.get("multimodal", {}).get("audio", False),
            streaming=True,
            function_calling=self.config.get("function_calling", False),
            json_mode=self.config.get("json_mode", False),
            reasoning_cot=self.config.get("reasoning_cot", False),
            code_generation=True,
            multilingual=True,
            max_context_window=self.config.get("context_window", 1000000),
            max_output_tokens=self.config.get("max_output_tokens", 8192),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
