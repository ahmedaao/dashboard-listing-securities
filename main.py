from src import compute_risk_adjusted_return


# Example usage:
security_returns = [12.5, 5.1, 15.2, -24.25, -5.85, 10]
benchmark_returns = [10, 8, 12, -20, -3, 9]

sharpe_ratio = compute_risk_adjusted_return.sharpe_ratio(
    security_returns, benchmark_returns
)
print("The Sharpe Ratio of the security relative to the benchmark is:", sharpe_ratio)
