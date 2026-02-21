import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# ==========================================
# 1. SETUP & DATA EXTRACTION
# ==========================================
TICKER = 'BTC-USD' # Changed from 'TSLA' to 'BTC-USD'
YEARS_TO_PREDICT = 1
TRADING_DAYS = 252
SIMULATIONS = 100

print(f"--- Quant Model Initialized for {TICKER} ---")

# Step 1: Get Real Data
# We look back 1 year to gauge how the stock is currently behaving
data = yf.download(TICKER, period="1y")

# Step 2: Calculate Real Volatility
data['Log Returns'] = np.log(data['Close'] / data['Close'].shift(1))
daily_volatility = data['Log Returns'].std()
annual_volatility = daily_volatility * np.sqrt(TRADING_DAYS)

# Step 3: Get the starting price (The most recent close)
last_price = data['Close'].iloc[-1].item() # .item() ensures we get a simple float number

print(f"Current Price: ${last_price:.2f}")
print(f"Real Annual Volatility: {annual_volatility*100:.2f}%")

# ==========================================
# 2. THE MONTE CARLO ENGINE
# ==========================================
def run_simulation(S, sigma, T, iterations):
    steps = TRADING_DAYS * T
    dt = 1/TRADING_DAYS
    r = 0.05 # Assuming 5% risk-free rate
    
    paths = np.zeros((steps + 1, iterations))
    paths[0] = S
    
    for t in range(1, steps + 1):
        Z = np.random.normal(0, 1, iterations)
        drift = (r - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt) * Z
        paths[t] = paths[t-1] * np.exp(drift + shock)
        
    return paths

print("Running simulations...")
future_paths = run_simulation(last_price, annual_volatility, YEARS_TO_PREDICT, SIMULATIONS)

# ==========================================
# 3. VISUALIZATION
# ==========================================
plt.figure(figsize=(12, 6))

# Plot the simulations
plt.plot(future_paths, color='blue', alpha=0.1) 

# Plot the average outcome (The "Expected" Path)
plt.plot(future_paths.mean(axis=1), color='red', linewidth=3, label='Average Path')

plt.title(f'{TICKER} Monte Carlo Simulation: Next {YEARS_TO_PREDICT} Year(s)', fontsize=14)
plt.xlabel(f'Trading Days ({TRADING_DAYS})')
plt.ylabel('Price ($)')
plt.axhline(y=last_price, color='black', linestyle=':', label='Start Price')
plt.legend()
plt.grid(True)
plt.show()

# Quick Stats
final_prices = future_paths[-1]
print("\n--- Forecast Statistics ---")
print(f"Worst Case (min): ${final_prices.min():.2f}")
print(f"Best Case (max):  ${final_prices.max():.2f}")
print(f"Average Outcome:  ${final_prices.mean():.2f}")