#!/usr/bin/env python3
"""Generates the final report."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.reporting.report import ReportGenerator
from src.utils.logger import logger

def main():
    logger.info("Generating reports...")
    generator = ReportGenerator()
    md_content = generator.generate_markdown()
    logger.info("Report generated successfully.")
    print("\n--- Final Report Preview ---\n")
    print(md_content)

if __name__ == "__main__":
    main()
