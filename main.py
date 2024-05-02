from src import compute_risk_adjusted_return


# Example usage:
security_returns = [12.5, 5.1, 15.2, -24.25, -5.85, 10]
benchmark_returns = [10, 8, 12, -20, -3, 9]
risk_free_rate = [3, 1, -1, 5, 2.4, 8.5]


a = compute_risk_adjusted_return.jensen_alpha(security_returns, benchmark_returns)
print(a)
