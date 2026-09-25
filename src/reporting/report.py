"""Generates Markdown and HTML reports."""
import json
import pandas as pd
from pathlib import Path

class ReportGenerator:
    def __init__(self, leaderboards_dir: str = "results/leaderboards", reports_dir: str = "results/reports"):
        self.leaderboards_dir = Path(leaderboards_dir)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_markdown(self) -> str:
        md = "# LLM Benchmarking Report\n\n"
        
        # Check if overall leaderboard exists
        overall_path = self.leaderboards_dir / "overall.csv"
        if overall_path.exists():
            df = pd.read_csv(overall_path)
            md += "## Overall Leaderboard\n\n"
            md += df.to_markdown(index=False)
            md += "\n\n"
            
        md += "## Detailed Breakdown\n"
        md += "Please check the individual CSV files in `results/leaderboards/` for specific metric breakdowns.\n"
        
        # Write to file
        with open(self.reports_dir / "report.md", "w") as f:
            f.write(md)
            
        return md
