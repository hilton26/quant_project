import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================
TICKER = 'SPY' # S&P 500 ETF (Liquid options)

print(f"Fetching Option Chain for {TICKER}...")
stock = yf.Ticker(TICKER)

# 1. Get Expiration Dates
expirations = stock.options
# Let's pick an expiration about 1-2 months out (usually the 3rd or 4th item)
expiry_date = expirations[2] 
print(f"Analyzing Expiry: {expiry_date}")

# 2. Get the Option Chain Data
chain = stock.option_chain(expiry_date)
calls = chain.calls

# 3. Filter Data
# We focus on strikes near the current price to see the 'Smile' clearly
current_price = stock.history(period='1d')['Close'].iloc[-1]
min_strike = current_price * 0.8
max_strike = current_price * 1.2

# Filter for liquid options (Volume > 0) to remove noise
filtered_calls = calls[
    (calls['strike'] > min_strike) & 
    (calls['strike'] < max_strike) &
    (calls['volume'] > 10)
]

# ==========================================
# PLOTTING THE SMILE
# ==========================================
plt.figure(figsize=(10, 6))

# Plot Strike vs Implied Volatility
# yfinance provides a pre-calculated 'impliedVolatility' column
plt.scatter(filtered_calls['strike'], filtered_calls['impliedVolatility'] * 100, 
            color='blue', alpha=0.6, label='Call Options IV')

# Add a polynomial trendline to visualize the curve "Smile"
z = np.polyfit(filtered_calls['strike'], filtered_calls['impliedVolatility'] * 100, 2)
p = np.poly1d(z)
plt.plot(filtered_calls['strike'], p(filtered_calls['strike']), "r--", label='Smile Trendline')

plt.title(f'Volatility Smile: {TICKER} (Exp: {expiry_date})', fontsize=14)
plt.xlabel('Strike Price ($)', fontsize=12)
plt.ylabel('Implied Volatility (%)', fontsize=12)
plt.axvline(x=current_price, color='black', linestyle=':', label=f'Current Price (${current_price:.0f})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()