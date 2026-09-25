"""Generates leaderboards from aggregated metrics."""
import pandas as pd
from pathlib import Path
from src.scoring.scorer import Scorer
from src.utils.logger import logger

class LeaderboardGenerator:
    def __init__(self, metrics_dir: str = "results/metrics", output_dir: str = "results/leaderboards"):
        self.metrics_dir = Path(metrics_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scorer = Scorer()
        
    def generate_all(self):
        metrics_file = self.metrics_dir / "aggregated_metrics.csv"
        if not metrics_file.exists():
            logger.error(f"Metrics file not found: {metrics_file}")
            return
            
        df = pd.read_csv(metrics_file)
        
        for lb_config in self.scorer.leaderboards:
            lb_id = lb_config["id"]
            logger.info(f"Generating leaderboard: {lb_id}")
            lb_df = self.scorer.calculate_leaderboard(df, lb_config)
            
            output_path = self.output_dir / f"{lb_id}.csv"
            lb_df.to_csv(output_path, index=False)
            
        logger.info(f"Generated {len(self.scorer.leaderboards)} leaderboards in {self.output_dir}")
