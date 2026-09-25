#!/usr/bin/env python3
"""Runs the benchmark engine."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmarking.engine import BenchmarkEngine
from src.providers.factory import get_all_model_ids
from src.utils.logger import logger
import dotenv

def main():
    dotenv.load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run LLM Benchmark")
    parser.add_argument("--model", type=str, required=True, help="Model ID or 'all'")
    parser.add_argument("--task", type=str, help="Specific task category to run")
    parser.add_argument("--methodology", type=str, default="controlled", help="Methodology to use")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without API calls")
    parser.add_argument("--workers", type=int, default=10, help="Max parallel workers")
    args = parser.parse_args()

    engine = BenchmarkEngine(max_workers=args.workers, dry_run=args.dry_run)
    
    models_to_run = get_all_model_ids() if args.model == "all" else [args.model]
    
    for model_id in models_to_run:
        logger.info(f"Starting benchmark for {model_id}...")
        try:
            engine.run_benchmark(model_id, args.task, args.methodology)
        except Exception as e:
            logger.error(f"Failed benchmark for {model_id}: {e}")
            
    logger.info("Benchmark complete.")

if __name__ == "__main__":
    main()
