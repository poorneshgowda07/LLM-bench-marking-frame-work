"""Defines benchmark methodologies (Controlled, Real-world, Adversarial)."""
from typing import Dict, Any
import yaml

class Methodology:
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.temperature = config.get("temperature", 0.0)
        self.max_tokens = config.get("max_tokens", 1024)
        self.top_p = config.get("top_p", 1.0)
        self.description = config.get("description", "")

    def get_options(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }

def load_methodologies(config_path: str = "configs/benchmark.yaml") -> Dict[str, Methodology]:
    with open(config_path) as f:
        config = yaml.safe_load(f)["benchmark"]["methodologies"]
    
    return {name: Methodology(name, data) for name, data in config.items()}
