"""Module containing metrics to compute"""

from typing import List
import numpy as np
from src.compute_function import rolling_variation


def beta(security_returns: List[float], benchmark_returns: List[float]):
    """
    Calculate the beta of a security relative to a benchmark.
    You can find the source here: Source: https://www.wallstreetmojo.com/beta-coefficient-calculate/
    Benchmark can be a portfolio of security returns or a index return

    Args:
        security_returns (List[float]): List of security returns.
        benchmark_returns (List[float]): List of benchmark returns.

    Returns:
        float: The calculated beta.
    """
    # Calculate percentage variation for security returns
    pct_change_security_returns = rolling_variation(security_returns, 2)

    # Calculate percentage variation for benchmark returns
    pct_change_benchmark_returns = rolling_variation(benchmark_returns, 2)

    # Calculate the covariance between security_returns and benchmark_returns
    covariance = np.cov(pct_change_benchmark_returns,
                        pct_change_security_returns)[0, 1]

    # Calculate the variance for benchmark_returns
    variance = np.var(pct_change_benchmark_returns)

    # Calculate beta metric
    compute_beta = covariance / variance

    return compute_beta
