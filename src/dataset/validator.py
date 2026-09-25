"""Validates dataset samples against the JSON schema."""
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from src.utils.logger import logger


class DatasetValidator:
    """Validates dataset JSONL files against the schema."""

    def __init__(self, schema_path: str = "data/schemas/dataset_schema.json"):
        self.schema_path = Path(schema_path)
        self._load_schema()

    def _load_schema(self):
        # We'll use basic validation here to avoid relying on heavy jsonschema package
        # but in production, we'd use jsonschema.validate()
        with open(self.schema_path) as f:
            self.schema = json.load(f)

    def validate_sample(self, sample: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a single sample."""
        errors = []
        required = self.schema.get("required", [])
        for field in required:
            if field not in sample:
                errors.append(f"Missing required field: {field}")
        
        if sample.get("task_category") not in self.schema["properties"]["task_category"]["enum"]:
            errors.append(f"Invalid task_category: {sample.get('task_category')}")
            
        if "difficulty" in sample and sample["difficulty"] not in self.schema["properties"]["difficulty"]["enum"]:
            errors.append(f"Invalid difficulty: {sample.get('difficulty')}")
            
        return len(errors) == 0, errors

    def validate_file(self, filepath) -> Tuple[bool, int, List[str]]:
        """Validate an entire JSONL file."""
        filepath = Path(filepath)
        errors = []
        valid_count = 0
        
        with open(filepath, encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                try:
                    sample = json.loads(line)
                    is_valid, sample_errors = self.validate_sample(sample)
                    if is_valid:
                        valid_count += 1
                    else:
                        errors.append(f"Line {i} invalid: {', '.join(sample_errors)}")
                except json.JSONDecodeError:
                    errors.append(f"Line {i} is not valid JSON")
                    
        if errors:
            logger.warning(f"Found {len(errors)} errors in {filepath.name}")
        else:
            logger.info(f"Validated {valid_count} samples in {filepath.name}")
            
        return len(errors) == 0, valid_count, errors
