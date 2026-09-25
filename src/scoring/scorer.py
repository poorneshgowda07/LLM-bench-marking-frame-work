"""Calculates weighted scores and leaderboards."""
import yaml
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


class Scorer:
    def __init__(self, scoring_config: str = "configs/scoring.yaml"):
        with open(scoring_config) as f:
            self.config = yaml.safe_load(f)["scoring"]
            
        self.default_weights = self.config["weights"]
        self.leaderboards = self.config["leaderboards"]

    def _normalize(self, df: pd.DataFrame, col: str, higher_is_better: bool = True):
        """Min-Max normalization to 0-100."""
        min_val = df[col].min()
        max_val = df[col].max()
        
        if max_val == min_val:
            return pd.Series([100.0] * len(df), index=df.index)
            
        if higher_is_better:
            normalized = (df[col] - min_val) / (max_val - min_val) * 100
        else:
            normalized = (max_val - df[col]) / (max_val - min_val) * 100
            
        return normalized

    def calculate_leaderboard(self, df: pd.DataFrame, leaderboard_config: Dict[str, Any]) -> pd.DataFrame:
        """Calculate scores for a specific leaderboard."""
        if "weights" in leaderboard_config and leaderboard_config["weights"] != "default":
            weights = leaderboard_config["weights"]
        else:
            weights = self.default_weights
            
        # Ensure we have all columns we need, default to 0 if missing
        required_cols = list(weights.keys())
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0.0
                
        # Copy df to avoid modifying original
        result_df = df.copy()
        
        # Normalize metrics before weighted sum
        # Assuming accuracy, multilingual, code, robustness are higher=better
        # latency, cost are lower=better
        # In this simple version, we assume metrics are pre-aggregated appropriately
        
        # We will directly compute a weighted sum for simplicity in this mock
        total_weight = sum(weights.values())
        
        score = pd.Series(0.0, index=result_df.index)
        for metric, weight in weights.items():
            if metric in result_df.columns:
                score += result_df[metric] * (weight / total_weight)
                
        result_df["total_score"] = score
        return result_df.sort_values(by="total_score", ascending=False)
