"""Collects evidence of failures and hallucinations."""
import json
from pathlib import Path
from typing import Dict, Any

class EvidenceCollector:
    def __init__(self, output_dir: str = "evidence/errors"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_failure(self, model_id: str, task_category: str, sample_id: str, prompt: str, prediction: str, reference: str, error_type: str = "general_failure"):
        """Save a failure record."""
        record = {
            "model_id": model_id,
            "task_category": task_category,
            "sample_id": sample_id,
            "error_type": error_type,
            "prompt": prompt,
            "prediction": prediction,
            "reference": reference
        }
        
        filepath = self.output_dir / f"{model_id}_{task_category}.json"
        
        # Append to existing or create new list
        if filepath.exists():
            with open(filepath, "r") as f:
                try:
                    records = json.load(f)
                except json.JSONDecodeError:
                    records = []
        else:
            records = []
            
        # check if already exists to avoid duplicates
        if not any(r["sample_id"] == sample_id for r in records):
            records.append(record)
            
            with open(filepath, "w") as f:
                json.dump(records, f, indent=2)
