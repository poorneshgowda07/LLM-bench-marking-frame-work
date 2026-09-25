"""Latency metrics calculation."""
from typing import List, Dict
import numpy as np


def calculate_latency_metrics(ttfts: List[float], tps_list: List[float], total_times: List[float]) -> Dict[str, float]:
    if not ttfts:
        return {}
        
    return {
        "ttft_mean": float(np.mean(ttfts)),
        "ttft_p50": float(np.percentile(ttfts, 50)),
        "ttft_p90": float(np.percentile(ttfts, 90)),
        "ttft_p95": float(np.percentile(ttfts, 95)),
        "ttft_p99": float(np.percentile(ttfts, 99)),
        
        "tps_mean": float(np.mean(tps_list)),
        "tps_p50": float(np.percentile(tps_list, 50)),
        
        "total_time_mean": float(np.mean(total_times)),
        "total_time_p90": float(np.percentile(total_times, 90))
    }
