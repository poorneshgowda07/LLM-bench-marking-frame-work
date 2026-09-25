"""Loads and standardizes dataset samples."""
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from src.dataset.validator import DatasetValidator
from src.hashing.hasher import hash_sample


class DatasetLoader:
    """Loads datasets defined in the tasks config."""

    def __init__(self, tasks_config_path: str = "configs/tasks.yaml"):
        self.config_path = Path(tasks_config_path)
        with open(self.config_path) as f:
            self.tasks_config = yaml.safe_load(f)["tasks"]
        self.validator = DatasetValidator()

    def load_task_dataset(self, task_id: str, validate: bool = True) -> List[Dict[str, Any]]:
        """Load the dataset for a specific task category."""
        if task_id not in self.tasks_config:
            raise ValueError(f"Task {task_id} not found in config")
            
        dataset_path = Path(self.tasks_config[task_id]["dataset_file"])
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
            
        if validate:
            is_valid, _, errors = self.validator.validate_file(dataset_path)
            if not is_valid:
                raise ValueError(f"Dataset validation failed: {errors[0]}")
                
        samples = []
        with open(dataset_path, encoding='utf-8') as f:
            for line in f:
                sample = json.loads(line)
                sample["sample_hash"] = hash_sample(sample)
                samples.append(sample)
                
        return samples

    def load_all_datasets(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load all datasets defined in the config."""
        datasets = {}
        for task_id in self.tasks_config:
            try:
                datasets[task_id] = self.load_task_dataset(task_id)
            except Exception as e:
                logger.error(f"Failed to load dataset for {task_id}: {e}")
        return datasets
