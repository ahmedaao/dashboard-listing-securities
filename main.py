from src import compute_risk_adjusted_return


# Example usage:
security_returns = [12.5, 5.1, 15.2, -24.25, -5.85, 10]
benchmark_returns = [10, 8, 12, -20, -3, 9]

from src.compute_metric import beta

a = beta([0.10, 0.20, 0.5, 0.20], [0.10, 0.20, 0.5, 0.20])
print(a)
