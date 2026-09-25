#!/usr/bin/env python3
"""Generates leaderboards."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.reporting.leaderboard import LeaderboardGenerator
from src.utils.logger import logger

def main():
    logger.info("Generating leaderboards...")
    generator = LeaderboardGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()
