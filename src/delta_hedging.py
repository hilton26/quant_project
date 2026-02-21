import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==========================================
# 1. SETUP PARAMETERS
# ==========================================
S0 = 100        # Initial Stock Price
K = 100         # Strike Price
T = 1.0         # Time to Maturity (1 Year)
r = 0.05        # Risk-Free Rate
sigma = 0.20    # Volatility (Implied & Realized are same for now)
steps = 252     # Re-hedging daily (252 times a year)
simulations = 1 # Just one path for clarity

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def bs_call_price(S, K, T, r, sigma):
    # Avoid division by zero at expiry
    if T <= 1e-5:
        return max(S - K, 0.0), 1.0 if S > K else 0.0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = (S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    delta = norm.cdf(d1)
    return price, delta

# ==========================================
# 3. SIMULATION LOOP
# ==========================================
dt = T / steps
time_axis = np.linspace(0, T, steps + 1)

# Generate Stock Path (GBM)
# We use a fixed seed so you get the same "random" path every time you run this
np.random.seed(42) 
W = np.random.normal(0, 1, steps)
stock_path = [S0]

for t in range(steps):
    # Standard GBM Formula
    drift = (r - 0.5 * sigma**2) * dt
    shock = sigma * np.sqrt(dt) * W[t]
    S_new = stock_path[-1] * np.exp(drift + shock)
    stock_path.append(S_new)

stock_path = np.array(stock_path)

# ==========================================
# 4. PERFORM DELTA HEDGING
# ==========================================
portfolio_values = []
cash_account = 0
stock_holdings = 0

# Initial Setup (t=0)
# We SOLD the Option, so we are Short the Option (-Price)
price, delta = bs_call_price(stock_path[0], K, T, r, sigma)
short_option_value = -price 

# We HEDGE by buying 'Delta' amount of shares
stock_holdings = delta
cash_account = -price - (stock_holdings * stock_path[0]) 
# Note: In real life, you receive premium (+price), but pay for stock (-cost).
# Here we track "Net Liquidation Value".

hedging_pnls = [0]

# Loop through every day
for t in range(1, steps + 1):
    S_curr = stock_path[t]
    time_left = T - time_axis[t]
    
    # 1. Update Option Value
    price, new_delta = bs_call_price(S_curr, K, time_left, r, sigma)
    
    # 2. Calculate P&L for this step
    # Change in Stock Value held + Change in Option Liability
    prev_S = stock_path[t-1]
    
    # P&L Attribution:
    # Stock Gain: We held 'stock_holdings' shares from yesterday
    stock_pnl = stock_holdings * (S_curr - prev_S)
    
    # Option Loss: The option price changed (remember we are short)
    # If price goes up, we lose money.
    # We estimate option price change using the previous step's data
    prev_price, _ = bs_call_price(prev_S, K, T - time_axis[t-1], r, sigma)
    option_pnl = -(price - prev_price) 
    
    # Interest: Cash earns 'r'
    # (Simplified for this view: ignoring cash drag on stock purchase for now)
    
    daily_pnl = stock_pnl + option_pnl
    hedging_pnls.append(daily_pnl)
    
    # 3. REBALANCE (The Hedge)
    # We need to own 'new_delta' shares. We currently own 'stock_holdings'.
    # We buy/sell the difference.
    stock_holdings = new_delta

cumulative_pnl = np.cumsum(hedging_pnls)

# ==========================================
# 5. VISUALIZATION
# ==========================================
fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Stock Price vs Strike
ax[0].plot(time_axis, stock_path, label='Stock Price', color='blue')
ax[0].axhline(y=K, color='black', linestyle='--', label='Strike ($100)')
ax[0].set_ylabel('Price ($)')
ax[0].set_title('Stock Price Movement')
ax[0].legend()
ax[0].grid(True)

# Bottom Plot: Hedging Error (Cumulative P&L)
ax[1].plot(time_axis, cumulative_pnl, label='Cumulative Hedging Error', color='red')
ax[1].axhline(y=0, color='black', linestyle=':', alpha=0.5)
ax[1].set_ylabel('P&L ($)')
ax[1].set_xlabel('Time (Years)')
ax[1].set_title('Hedging P&L (Ideally Zero)')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

print(f"Final Hedging Error: ${cumulative_pnl[-1]:.2f}")