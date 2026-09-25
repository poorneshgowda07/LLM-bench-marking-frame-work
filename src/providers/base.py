"""Abstract base class for all LLM provider adapters."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional
import time


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""

    # Core output
    prediction: str
    model: str
    provider: str

    # Token counts
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    # Latency (all in seconds)
    ttft: float = 0.0          # Time to First Token
    total_time: float = 0.0    # End-to-end wall clock time
    tokens_per_second: float = 0.0

    # Metadata
    timestamp: str = ""
    prompt_hash: str = ""
    run_id: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    # Cost
    cost_usd: float = 0.0

    # Error info
    error: Optional[str] = None
    is_error: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for JSON storage."""
        return {
            "prediction": self.prediction,
            "model": self.model,
            "provider": self.provider,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "ttft": self.ttft,
            "total_time": self.total_time,
            "tokens_per_second": self.tokens_per_second,
            "timestamp": self.timestamp,
            "prompt_hash": self.prompt_hash,
            "run_id": self.run_id,
            "cost_usd": self.cost_usd,
            "error": self.error,
            "is_error": self.is_error,
        }


@dataclass
class CapabilityMatrix:
    """Documents what a model can and cannot do."""
    vision: bool = False
    audio: bool = False
    streaming: bool = True
    function_calling: bool = False
    json_mode: bool = False
    reasoning_cot: bool = False
    code_generation: bool = True
    multilingual: bool = True
    fine_tuning: bool = False
    max_context_window: int = 4096
    max_output_tokens: int = 1024
    pricing_input_per_1m: float = 0.0
    pricing_output_per_1m: float = 0.0


class LLMProvider(ABC):
    """Abstract base class for all LLM provider adapters.

    To add a new provider:
    1. Create a new directory under src/providers/<provider_name>/
    2. Create provider.py implementing this class
    3. Register in src/providers/factory.py

    The system is designed so adding a new provider requires
    ONLY creating a new adapter — the benchmark engine is unaffected.
    """

    def __init__(self, model_id: str, config: Dict[str, Any]):
        self.model_id = model_id
        self.config = config
        self.provider_name = config.get("provider", "unknown")

    @abstractmethod
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        """Send a completion request and return a standardized LLMResponse.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system/instruction prompt.
            options: Runtime options (temperature, max_tokens, etc.).

        Returns:
            LLMResponse with prediction, latency, and token counts.
        """
        pass

    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        """Stream completion tokens. Default: fall back to non-streaming."""
        response = self.complete(prompt, system_prompt, options)
        yield response.prediction

    def get_capabilities(self) -> CapabilityMatrix:
        """Return the capability matrix for this model."""
        return CapabilityMatrix()

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD based on token counts and pricing config."""
        caps = self.get_capabilities()
        cost = (
            (input_tokens * caps.pricing_input_per_1m / 1_000_000)
            + (output_tokens * caps.pricing_output_per_1m / 1_000_000)
        )
        return round(cost, 8)

    def health_check(self) -> bool:
        """Verify the provider is reachable. Override for custom checks."""
        try:
            resp = self.complete("Say OK", options={"max_tokens": 10})
            return not resp.is_error
        except Exception:
            return False
