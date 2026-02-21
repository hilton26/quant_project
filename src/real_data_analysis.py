import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================
TICKER = 'TSLA'  # Try 'AAPL', 'GOOG', 'MSFT', 'BTC-USD'
START_DATE = '2025-01-01'
END_DATE = '2026-01-01'

def analyze_stock(ticker, start, end):
    print(f"Downloading data for {ticker}...")
    
    # 1. Download Data
    df = yf.download(ticker, start=start, end=end)
    
    # 2. Calculate Daily Log Returns
    # Log returns are preferred by Quants over simple percentage change
    # Formula: ln(Today / Yesterday)
    df['Log Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # 3. Calculate Volatility (Standard Deviation)
    # We drop the first row (NaN) created by the shift
    daily_volatility = df['Log Returns'].std()
    
    # 4. Annualize the Volatility
    # We multiply by square root of 252 (trading days in a year)
    annual_volatility = daily_volatility * np.sqrt(252)
    
    print(f"\n--- Results for {ticker} ---")
    print(f"Annualized Volatility: {annual_volatility*100:.2f}%")
    
    return df, annual_volatility

# ==========================================
# EXECUTION & PLOTTING
# ==========================================

data, vol = analyze_stock(TICKER, START_DATE, END_DATE)

# Plotting the Closing Price
plt.figure(figsize=(10, 6))
plt.plot(data['Close'], label=f'{TICKER} Price')
plt.title(f'{TICKER} Price History (Vol: {vol*100:.2f}%)')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the Daily Returns (The "Noise")
plt.figure(figsize=(10, 4))
plt.plot(data['Log Returns'], color='orange', alpha=0.6)
plt.title(f'{TICKER} Daily Log Returns')
plt.grid(True)
plt.show()