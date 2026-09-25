#!/usr/bin/env python3
"""Validates and prepares datasets."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dataset.loader import DatasetLoader
from src.utils.logger import logger

def main():
    logger.info("Starting dataset preparation...")
    loader = DatasetLoader()
    
    try:
        datasets = loader.load_all_datasets()
        total_samples = sum(len(samples) for samples in datasets.values())
        logger.info(f"Successfully validated {total_samples} samples across {len(datasets)} categories.")
    except Exception as e:
        logger.error(f"Dataset preparation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
