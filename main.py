from src.metric import compute_risk_adjusted_return
from src.metric import compute_return
import yfinance as yf


# Example usage:
security_returns = [12.5, 5.1, 15.2, -24.25, -5.85, 10]
benchmark_returns = [10, 8, 12, -20, -3, 9]
risk_free_rate = [3, 1, -1, 5, 2.4, 8.5]


a = compute_risk_adjusted_return.jensen_alpha(
    security_returns, benchmark_returns, risk_free_rate
)
print(a)
print()

current_price = 3000000
original_price = 30000000
days_held = 3650

cumulative_return = compute_return.cumulative_return(126000, 100000)
print(cumulative_return)

annualized_return = compute_return.annualized_return(days_held, cumulative_return)
print(annualized_return)

print()

current_price = 200000
required_price = 5000000
nb_years = 10
a = compute_return.required_annualized_return(current_price, required_price, nb_years)
# print(a)

df = yf.download(["TSLA", "PEP"], period="5y", interval="1mo")

close = df.Close
# print(close)


tsla = yf.Ticker("TSLA")
history = tsla.history(start="2024-06-01")
print(history.Open[1])
