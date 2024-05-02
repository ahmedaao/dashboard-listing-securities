"""Module containing functions which compute risk-adjusted return"""

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


def sharpe_ratio(security_returns: List[float],
                 benchmark_returns: List[float]) -> dict:
    """
    Calculate the Sharpe Ratio of a security relative to a benchmark.
    You can find the source here: Source: https://www.wallstreetmojo.com/risk-adjusted-returns/
    Benchmark can be the risk-free rate returns or index returns

    Args:
        security_returns (List[float]): List of security returns.
        benchmark_returns (List[float]): List of benchmark returns.

    Returns:
        float: The calculated Sharpe Ratio.
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
        "mean_security_return": mean_security_return,
        "mean_benchmark_return": mean_benchmark_return,
        "std_dev_security": std_dev_security,
        "excess_return": excess_return,
        "compute_sharpe_ratio": compute_sharpe_ratio,
    }


def treynor_ratio(
    security_returns: List[float], benchmark_returns: List[float]
) -> dict:
    """
    Calculate the Treynor Ratio of a security relative to a benchmark.
    Benchmark can be the risk-free rate returns or index returns
    Source: https://www.wallstreetmojo.com/risk-adjusted-returns/

    Args:
        security_returns (List[float]): List of security returns.
        benchmark_returns (List[float]): List of benchmark returns.

    Returns:
        float: The calculated Sharpe Ratio.
    """
    # Calculate mean portfolio return
    mean_security_return = np.mean(security_returns)

    # Calculate mean benchmark return
    mean_benchmark_return = np.mean(benchmark_returns)

    # Calculate the beta for the security relative to benchmark returns
    compute_beta = beta(security_returns, benchmark_returns)

    # Calculate excess return of portfolio over benchmark
    excess_return = mean_security_return - mean_benchmark_return

    # Calculate Sharpe Ratio
    compute_treynor_ratio = excess_return / compute_beta

    return {"compute_treynor_ratio": compute_treynor_ratio}


def jensen_alpha(
    expected_portfolio_return: List[float],
    benchmark_return: List[float],
    risk_free_rate: List[float],
) -> dict:
    """
    Calculate the Jensen's Alpha of a portfolio relative to a benchmark.
    You can find the source here: Source: https://www.wallstreetmojo.com/risk-adjusted-returns/
    Benchmark is generally a index (s&p500 or others)

    Args:
        expected_portfolio_return (List[float]): List of portfolio return.
        benchmark_return (List[float]): List of benchmark return.
        risk_free_rate (List[float]): List of risk free rate

    Returns:
        float: The calculated Jensen's Alpha Ratio.
    """
    # Calculate mean expected portfolio return
    mean_expected_portfolio_return = np.mean(expected_portfolio_return)

    # Calculate mean benchmark return
    mean_benchmark_return = np.mean(benchmark_return)

    # Calculate mean risk free rate
    mean_risk_free_rate = np.mean(risk_free_rate)

    # Calculate the beta of the portfolio
    compute_beta = beta(expected_portfolio_return, benchmark_return)

    # Calculate Jensen's Alpha Ratio
    compute_alpha_ratio = (
        mean_expected_portfolio_return
        - mean_risk_free_rate
        - compute_beta * (mean_benchmark_return - mean_risk_free_rate)
    )

    return {"compute_alpha_ratio": compute_alpha_ratio}
