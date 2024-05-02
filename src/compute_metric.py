# Import packages
from typing import List
import numpy as np
import pandas as pd


def beta(security_returns: List[float], benchmark_returns: List[float]) -> dict:
    """
    Calculate the beta of a security relative to a benchmark.
    You can find the source here: Source: https://www.wallstreetmojo.com/beta-coefficient-calculate/
    Benchmark can be a portfolio return or a index return

    Args:
        security_returns (List[float]): List of security returns.
        benchmark_returns (List[float]): List of benchmark returns.

    Returns:
        float: The calculated beta.
    """
    # Calculate mean portfolio return
    mean_security_return = np.mean(security_returns)

    # Calculate mean benchmark return
    mean_benchmark_return = np.mean(benchmark_returns)

    # Calculate standard deviation of portfolio returns
    std_dev_security = np.std(security_returns)

    # Calculate excess return of portfolio over benchmark
    excess_return = mean_security_return - mean_benchmark_return

    # Calculate Sharpe Ratio
    compute_sharpe_ratio = excess_return / std_dev_security
    # rounded_compute_sharpe_ratio = round(compute_sharpe_ratio, 2)

    return {
        "beta": beta
    }
