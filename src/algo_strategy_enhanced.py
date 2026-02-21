import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EnhancedTradingBot:
    def __init__(self, ticker, start_date, short_window=50, long_window=200, rsi_limit=70):
        self.ticker = ticker
        self.start = start_date
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_limit = rsi_limit  # the safety cutoff
        self.data = None
        
    def download_data(self):
        print(f"Downloading data for {self.ticker}...")
        # Download the raw data
        raw_data = yf.download(self.ticker, start=self.start, progress=False)
        # --- THE FIX ---
        # Check if the data has a complex "MultiIndex" structure (common in new yfinance)
        # If it does, we strip away the Ticker level to make it a simple table.
        if isinstance(raw_data.columns, pd.MultiIndex):
            raw_data.columns = raw_data.columns.droplevel(1)
            
        # Now we can safely select 'Close' as a clean DataFrame
        self.data = raw_data[['Close']].copy()
        
    def add_indicators(self):
        """
        Calculates RSI, MACD, and Bollinger Bands manually using Pandas.
        """
        # --- 1. MACD (Moving Average Convergence Divergence) ---
        # EMA (Exponential Moving Average) 12 and 26
        ema12 = self.data['Close'].ewm(span=12, adjust=False).mean()
        ema26 = self.data['Close'].ewm(span=26, adjust=False).mean()
        self.data['MACD_Line'] = ema12 - ema26
        self.data['Signal_Line'] = self.data['MACD_Line'].ewm(span=9, adjust=False).mean()
        
        # --- 2. RSI (Relative Strength Index) ---
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # --- 3. Bollinger Bands (Volatility) ---
        # 20-day SMA
        self.data['BB_Middle'] = self.data['Close'].rolling(window=20).mean()
        # Standard Deviation
        std_dev = self.data['Close'].rolling(window=20).std()
        self.data['BB_Upper'] = self.data['BB_Middle'] + (2 * std_dev)
        self.data['BB_Lower'] = self.data['BB_Middle'] - (2 * std_dev)

        # --- 4. Standard Moving Averages (for the base trend) ---
        self.data['Short_SMA'] = self.data['Close'].rolling(window=50).mean()
        self.data['Long_SMA'] = self.data['Close'].rolling(window=200).mean()

    def generate_signals(self):
        """
        Strategy: Golden Cross + RSI Filter.
        Buy when: 50 SMA > 200 SMA (Trend is Up) AND RSI < 70 (Not Overbought).
        Sell when: 50 SMA < 200 SMA.
        """
        self.data.dropna(inplace=True) # Remove empty rows needed for calculation
        
        self.data['Signal'] = 0.0
        
        # Define the conditions
        # Use the variables (self.short_window, etc.) instead of raw numbers
        golden_cross = self.data['Short_SMA'] > self.data['Long_SMA']
        
        # Use the variable self.rsi_limit
        rsi_filter = self.data['RSI'] < self.rsi_limit # Only buy if we have room to grow
        
        # Apply Logic: If Golden Cross is Active AND RSI is healthy -> Signal 1 (Hold/Buy)
        self.data.loc[golden_cross & rsi_filter, 'Signal'] = 1.0
        
        # Calculate Positions (1 = Buy, -1 = Sell)
        self.data['Position'] = self.data['Signal'].diff()

    def plot_dashboard(self):
        """
        Creates a Professional Trading Dashboard with 3 panels.
        """
        plt.figure(figsize=(14, 10))
        
        # --- Panel 1: Price, SMAs, and Bollinger Bands ---
        ax1 = plt.subplot(3, 1, 1)
        ax1.plot(self.data['Close'], label='Price', color='black', alpha=0.6)
        ax1.plot(self.data['Short_SMA'], label='SMA 50', color='blue', alpha=0.7)
        ax1.plot(self.data['Long_SMA'], label='SMA 200', color='orange', alpha=0.7)
        # Plot Bollinger Bands area
        ax1.fill_between(self.data.index, self.data['BB_Upper'], self.data['BB_Lower'], color='gray', alpha=0.1, label='Volatility (BB)')
        
        # Plot Buy/Sell Markers
        buys = self.data[self.data['Position'] == 1]
        sells = self.data[self.data['Position'] == -1]
        ax1.scatter(buys.index, buys['Close'], marker='^', color='green', s=100, label='Buy')
        ax1.scatter(sells.index, sells['Close'], marker='v', color='red', s=100, label='Sell')
        
        ax1.set_title(f'{self.ticker} Price & Volatility')
        ax1.legend(loc='upper left')
        ax1.grid(True)

        # --- Panel 2: MACD (Momentum) ---
        ax2 = plt.subplot(3, 1, 2, sharex=ax1)
        ax2.plot(self.data['MACD_Line'], label='MACD', color='purple')
        ax2.plot(self.data['Signal_Line'], label='Signal', color='orange', linestyle='--')
        # Draw a histogram for the difference
        ax2.bar(self.data.index, self.data['MACD_Line'] - self.data['Signal_Line'], color='gray', alpha=0.3)
        ax2.set_title('MACD (Momentum)')
        ax2.grid(True)
        
        # --- Panel 3: RSI (Overbought/Oversold) ---
        ax3 = plt.subplot(3, 1, 3, sharex=ax1)
        ax3.plot(self.data['RSI'], color='blue')
        ax3.axhline(70, color='red', linestyle='--', label='Overbought')
        ax3.axhline(30, color='green', linestyle='--', label='Oversold')
        ax3.set_title('RSI (Strength)')
        ax3.set_ylim(0, 100)
        ax3.grid(True)
        
        plt.tight_layout()
        plt.show()

# # ============================
# # RUN THE BOT
# # ============================
# # Try 'NVDA' (Nvidia) or 'BTC-USD'
# bot = EnhancedTradingBot('BTC-USD', start_date='2022-01-01')
# bot.download_data()
# bot.add_indicators()
# bot.generate_signals()
# bot.plot_dashboard()


# ==========================================
# SCENARIO A: THE "SCALPER" (Aggressive)
# ==========================================
# Logic: Look at the last 10 days vs 50 days. 
# Buy even if RSI is high (80). We want speed!
print("Running Aggressive Bot...")
bot_fast = EnhancedTradingBot('TSLA', start_date='2023-01-01', 
                              short_window=10, 
                              long_window=50, 
                              rsi_limit=80)
bot_fast.download_data()
bot_fast.add_indicators()
bot_fast.generate_signals()
bot_fast.plot_dashboard()

# ==========================================
# SCENARIO B: THE "INVESTOR" (Conservative)
# ==========================================
# Logic: Look at the last 50 days vs 200 days.
# Only buy if RSI is very safe (below 60). We want certainty.
print("Running Conservative Bot...")
bot_slow = EnhancedTradingBot('TSLA', start_date='2023-01-01',
                              short_window=50, 
                              long_window=200, 
                              rsi_limit=60)
bot_slow.download_data()
bot_slow.add_indicators()
bot_slow.generate_signals()
bot_slow.plot_dashboard()