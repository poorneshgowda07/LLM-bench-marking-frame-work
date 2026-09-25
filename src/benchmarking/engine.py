"""Core benchmarking engine that orchestrates running models against datasets."""
import json
import os
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, List, Optional
from tqdm import tqdm
from datetime import datetime

from src.providers.factory import get_provider
from src.dataset.loader import DatasetLoader
from src.benchmarking.methodologies import load_methodologies
from src.utils.logger import logger
from src.hashing.hasher import hash_prompt, hash_result


class BenchmarkEngine:
    def __init__(self, max_workers: int = 10, dry_run: bool = False):
        self.max_workers = max_workers
        self.dry_run = dry_run
        self.dataset_loader = DatasetLoader()
        self.methodologies = load_methodologies()
        
        self.raw_results_dir = Path("results/raw")
        self.raw_results_dir.mkdir(parents=True, exist_ok=True)

    def _get_result_path(self, model_id: str, task_category: str, methodology: str, sample_id: str) -> Path:
        dir_path = self.raw_results_dir / model_id / task_category / methodology
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / f"{sample_id}.json"

    def run_sample(self, provider, sample: Dict[str, Any], methodology_name: str) -> Optional[Dict[str, Any]]:
        methodology = self.methodologies[methodology_name]
        result_path = self._get_result_path(provider.model_id, sample["task_category"], methodology_name, sample["id"])
        
        # Skip if already run
        if result_path.exists():
            return None

        prompt = sample["prompt"]
        options = methodology.get_options()
        prompt_hash = hash_prompt(prompt, provider.model_id, options)
        
        if self.dry_run:
            logger.info(f"[Dry Run] Would execute {sample['id']} on {provider.model_id}")
            return None

        response = provider.complete(prompt, options=options)
        
        result = {
            "sample_id": sample["id"],
            "model": provider.model_id,
            "task_category": sample["task_category"],
            "methodology": methodology_name,
            "prompt_hash": prompt_hash,
            "response": response.to_dict(),
            "reference": sample.get("reference"),
            "timestamp": datetime.now().isoformat()
        }
        result["result_hash"] = hash_result({
            "sample_id": result["sample_id"],
            "model": result["model"],
            "prediction": response.prediction,
            "prompt_hash": prompt_hash
        })
        
        with open(result_path, "w") as f:
            json.dump(result, f, indent=2)
            
        return result

    def run_benchmark(self, model_id: str, task_category: Optional[str] = None, methodology_name: str = "controlled"):
        provider = get_provider(model_id)
        if not provider.health_check() and not self.dry_run:
            logger.warning(f"Provider {model_id} failed health check. Proceeding anyway, but errors may occur.")

        if task_category:
            datasets = {task_category: self.dataset_loader.load_task_dataset(task_category)}
        else:
            datasets = self.dataset_loader.load_all_datasets()
            
        for t_cat, samples in datasets.items():
            if methodology_name == "adversarial" and t_cat != "adversarial":
                continue # Skip non-adversarial tasks if adversarial method chosen
                
            logger.info(f"Running {len(samples)} samples for {model_id} on {t_cat} ({methodology_name})")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [
                    executor.submit(self.run_sample, provider, sample, methodology_name) 
                    for sample in samples
                ]
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Error executing sample: {e}")
