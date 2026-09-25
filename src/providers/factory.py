"""Provider factory — maps model IDs to their adapter instances."""
from typing import Any, Dict
import yaml
from pathlib import Path


def load_model_config(model_id: str) -> Dict[str, Any]:
    """Load model configuration from configs/models.yaml."""
    config_path = Path(__file__).parent.parent.parent / "configs" / "models.yaml"
    with open(config_path) as f:
        all_models = yaml.safe_load(f)["models"]
    if model_id not in all_models:
        raise ValueError(f"Unknown model '{model_id}'. Check configs/models.yaml.")
    return all_models[model_id]


def load_provider_config(provider: str) -> Dict[str, Any]:
    """Load provider configuration from configs/providers.yaml."""
    config_path = Path(__file__).parent.parent.parent / "configs" / "providers.yaml"
    with open(config_path) as f:
        all_providers = yaml.safe_load(f)["providers"]
    if provider not in all_providers:
        raise ValueError(f"Unknown provider '{provider}'. Check configs/providers.yaml.")
    return all_providers[provider]


def get_provider(model_id: str):
    """Factory function: returns an initialized LLMProvider for the given model ID.

    Usage:
        provider = get_provider('gpt-4o')
        response = provider.complete('Hello!')
    """
    from src.providers.base import LLMProvider

    model_config = load_model_config(model_id)
    provider_name = model_config["provider"]
    provider_config = load_provider_config(provider_name)

    # Merge model config into provider config for the adapter
    merged = {**provider_config, **model_config}

    if provider_name == "openai":
        from src.providers.openai.provider import OpenAIProvider
        return OpenAIProvider(model_id=model_id, config=merged)
    elif provider_name == "google":
        from src.providers.google.provider import GoogleProvider
        return GoogleProvider(model_id=model_id, config=merged)
    elif provider_name == "anthropic":
        from src.providers.anthropic.provider import AnthropicProvider
        return AnthropicProvider(model_id=model_id, config=merged)
    elif provider_name == "meta":
        from src.providers.meta.provider import MetaProvider
        return MetaProvider(model_id=model_id, config=merged)
    elif provider_name == "deepseek":
        from src.providers.deepseek.provider import DeepSeekProvider
        return DeepSeekProvider(model_id=model_id, config=merged)
    elif provider_name == "mistral":
        from src.providers.mistral.provider import MistralProvider
        return MistralProvider(model_id=model_id, config=merged)
    elif provider_name == "mock":
        from src.providers.mock import MockProvider
        return MockProvider(model_id=model_id, config=merged)
    else:
        raise ValueError(f"No adapter registered for provider '{provider_name}'.")


def get_all_model_ids() -> list:
    """Return all model IDs from the model registry."""
    config_path = Path(__file__).parent.parent.parent / "configs" / "models.yaml"
    with open(config_path) as f:
        return list(yaml.safe_load(f)["models"].keys())
