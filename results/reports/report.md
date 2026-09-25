# LLM Benchmarking Report

## Overall Leaderboard

| model           |   accuracy_quality |   f1 |   latency_speed |   total_time |   cost_efficiency |   robustness_safety |   multilingual |   code_generation |   context_window |   total_score |
|:----------------|-------------------:|-----:|----------------:|-------------:|------------------:|--------------------:|---------------:|------------------:|-----------------:|--------------:|
| gemini-2.5-pro  |               87.8 | 0.88 |           -0.85 |          3.2 |            -11.25 |                0.97 |           91   |              88.5 |          1000000 |      50042.5  |
| claude-sonnet-4 |               89.2 | 0.91 |           -0.6  |          2.8 |            -15    |                0.99 |           86.5 |              94.5 |           200000 |      10042.6  |
| llama-3.3-70b   |               82.1 | 0.83 |           -0.55 |          2.5 |             -0.88 |                0.92 |           71.5 |              81   |           131072 |       6593.33 |
| gpt-4o          |               88.5 | 0.89 |           -0.45 |          2.1 |            -12.5  |                0.98 |           87.2 |              92.1 |           128000 |       6442.61 |
| deepseek-v3     |               85   | 0.86 |           -0.75 |          3   |             -1.37 |                0.9  |           82   |              89.5 |           128000 |       6442.38 |
| gpt-4o-mini     |               78.5 | 0.79 |           -0.25 |          1.2 |             -0.75 |                0.95 |           75   |              79.2 |           128000 |       6438.9  |

## Detailed Breakdown
Please check the individual CSV files in `results/leaderboards/` for specific metric breakdowns.
