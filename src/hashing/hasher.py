"""SHA-256 hashing for reproducibility of benchmark runs."""
import hashlib
import json
from typing import Any, Dict


def hash_prompt(prompt: str, model: str = "", options: Dict[str, Any] = None) -> str:
    """Generate a deterministic SHA-256 hash for a prompt + model + options combo.

    This hash acts as a unique fingerprint for each (prompt, model, config)
    combination, enabling reproducibility and regression testing.
    """
    payload = {
        "prompt": prompt,
        "model": model,
        "options": options or {},
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def hash_sample(sample: Dict[str, Any]) -> str:
    """Hash a dataset sample (prompt + reference)."""
    key_fields = {"id": sample.get("id", ""), "prompt": sample.get("prompt", ""), "reference": sample.get("reference", "")}
    serialized = json.dumps(key_fields, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def hash_result(result: Dict[str, Any]) -> str:
    """Hash a raw LLM result for integrity verification."""
    key_fields = {
        "sample_id": result.get("sample_id"),
        "model": result.get("model"),
        "prediction": result.get("prediction"),
        "prompt_hash": result.get("prompt_hash"),
    }
    serialized = json.dumps(key_fields, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
