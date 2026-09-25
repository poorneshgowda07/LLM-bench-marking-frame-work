"""Meta Llama provider — Llama 4 Scout/Maverick, Llama 3.3 70B via Together AI or Ollama."""
import os
import time
from typing import Any, Dict, Iterator, Optional
from datetime import datetime, timezone

from src.providers.base import LLMProvider, LLMResponse, CapabilityMatrix
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger


class MetaProvider(LLMProvider):
    """Adapter for Meta Llama models via Together AI API or local Ollama.

    Backend selection:
    - If TOGETHER_API_KEY is set → Together AI (primary)
    - If OLLAMA_BASE_URL is set and no Together key → Ollama (local)
    """

    def __init__(self, model_id: str, config: Dict[str, Any]):
        super().__init__(model_id=model_id, config=config)
        self.api_model_id = config.get("api_model_id", model_id)
        self._pricing = config.get("pricing", {"input_per_1m": 0, "output_per_1m": 0})
        self._backend = self._detect_backend()

    def _detect_backend(self) -> str:
        if os.environ.get("TOGETHER_API_KEY"):
            return "together"
        if os.environ.get("OLLAMA_BASE_URL"):
            return "ollama"
        raise EnvironmentError(
            "Meta models require either TOGETHER_API_KEY (Together AI) or "
            "OLLAMA_BASE_URL (local Ollama) to be set."
        )

    def _get_together_client(self):
        try:
            from together import Together
            return Together(api_key=os.environ["TOGETHER_API_KEY"])
        except ImportError:
            raise ImportError("together package not installed. Run: pip install together")

    def _get_ollama_client(self):
        try:
            import ollama
            return ollama
        except ImportError:
            raise ImportError("ollama package not installed. Run: pip install ollama")

    @retry_with_backoff(max_retries=3, backoff_factor=2.0)
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        opts = options or {}
        if self._backend == "together":
            return self._together_complete(prompt, system_prompt, opts)
        else:
            return self._ollama_complete(prompt, system_prompt, opts)

    def _together_complete(self, prompt, system_prompt, opts) -> LLMResponse:
        client = self._get_together_client()
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
            stream = client.chat.completions.create(
                model=self.api_model_id,
                messages=messages,
                max_tokens=opts.get("max_tokens", 1024),
                temperature=opts.get("temperature", 0.0),
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else ""
                if delta:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += delta
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
                prediction=full_text.strip(), model=self.model_id, provider="meta",
                input_tokens=input_tokens, output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4), total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=self.calculate_cost(input_tokens, output_tokens),
            )
        except Exception as e:
            logger.error(f"[Meta/Together] Error: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="meta",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def _ollama_complete(self, prompt, system_prompt, opts) -> LLMResponse:
        import ollama
        ollama_model = self.api_model_id.split("/")[-1].lower().replace("-instruct", "")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start_time = time.perf_counter()
        first_token_time = None
        full_text = ""

        try:
            stream = ollama.chat(model=ollama_model, messages=messages, stream=True)
            for chunk in stream:
                content = chunk["message"]["content"]
                if content:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    full_text += content

            total_time = time.perf_counter() - start_time
            ttft = (first_token_time - start_time) if first_token_time else total_time
            output_tokens = len(full_text.split())
            input_tokens = len(prompt.split())
            tps = output_tokens / max(total_time - ttft, 0.001)

            return LLMResponse(
                prediction=full_text.strip(), model=self.model_id, provider="meta",
                input_tokens=input_tokens, output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                ttft=round(ttft, 4), total_time=round(total_time, 4),
                tokens_per_second=round(tps, 2),
                timestamp=datetime.now(timezone.utc).isoformat(),
                cost_usd=0.0,  # Local inference is free
            )
        except Exception as e:
            logger.error(f"[Meta/Ollama] Error: {e}")
            return LLMResponse(
                prediction="", model=self.model_id, provider="meta",
                error=str(e), is_error=True,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

    def stream_complete(self, prompt, system_prompt=None, options=None) -> Iterator[str]:
        response = self.complete(prompt, system_prompt, options)
        yield response.prediction

    def get_capabilities(self) -> CapabilityMatrix:
        p = self._pricing
        return CapabilityMatrix(
            vision=self.config.get("multimodal", {}).get("vision", False),
            streaming=True,
            function_calling=self.config.get("function_calling", False),
            json_mode=self.config.get("json_mode", False),
            code_generation=True, multilingual=True,
            max_context_window=self.config.get("context_window", 131072),
            max_output_tokens=self.config.get("max_output_tokens", 4096),
            pricing_input_per_1m=p.get("input_per_1m", 0),
            pricing_output_per_1m=p.get("output_per_1m", 0),
        )
