import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MovingAverageBot:
    def __init__(self, ticker, start_date, short_window=50, long_window=200):
        self.ticker = ticker
        self.start = start_date
        self.short_window = short_window
        self.long_window = long_window
        self.data = None
        
    def download_data(self):
        print(f"Downloading data for {self.ticker}...")
        self.data = yf.download(self.ticker, start=self.start, progress=False)
        # Ensure we have a clean DataFrame
        self.data = self.data[['Close']].copy()
        
    def generate_signals(self):
        """
        Calculates moving averages and determines where to Buy/Sell.
        """
        # 1. Calculate the Moving Averages (SMA)
        self.data['Short_SMA'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['Long_SMA']  = self.data['Close'].rolling(window=self.long_window).mean()
        
        # 2. Create a 'Signal' Column (0.0 means do nothing)
        self.data['Signal'] = 0.0
        
        # 3. Set Signal to 1.0 where Short > Long
        # We start from the index 'short_window' to avoid NaNs
        self.data.loc[self.data.index[self.short_window:], 'Signal'] = \
            np.where(self.data['Short_SMA'][self.short_window:] > 
                     self.data['Long_SMA'][self.short_window:], 1.0, 0.0)
            
        # 4. Generate 'Positions' (The Trading Orders)
        # diff() checks the difference between today's signal and yesterday's.
        # +1 = Buy (0 -> 1), -1 = Sell (1 -> 0)
        self.data['Position'] = self.data['Signal'].diff()

    def backtest(self):
        """
        Simulates how much money we would have made.
        """
        initial_capital = 10000.0
        
        # Calculate Daily Market Returns (Percentage Change)
        self.data['Market_Returns'] = self.data['Close'].pct_change()
        
        # Calculate Strategy Returns
        # We shift the signal by 1 day because we trade AT THE OPEN of the *next* day
        # based on the crossover that happened at the *close* of the previous day.
        self.data['Strategy_Returns'] = self.data['Market_Returns'] * self.data['Signal'].shift(1)
        
        # Calculate Cumulative Returns
        self.data['Cumulative_Market'] = (1 + self.data['Market_Returns']).cumprod() * initial_capital
        self.data['Cumulative_Strategy'] = (1 + self.data['Strategy_Returns']).cumprod() * initial_capital
        
        final_val = self.data['Cumulative_Strategy'].iloc[-1]
        print(f"Final Portfolio Value: ${final_val:.2f}")
        return final_val

    def plot_results(self):
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Price and SMAs
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(self.data['Close'], label='Price', alpha=0.5)
        ax1.plot(self.data['Short_SMA'], label=f'SMA {self.short_window}', alpha=0.8)
        ax1.plot(self.data['Long_SMA'], label=f'SMA {self.long_window}', alpha=0.8)
        
        # Plot Buy Signals (Green Triangles)
        ax1.plot(self.data.loc[self.data.Position == 1.0].index, 
                 self.data.Short_SMA[self.data.Position == 1.0], 
                 '^', markersize=10, color='g', label='Buy Signal')
        
        # Plot Sell Signals (Red Triangles)
        ax1.plot(self.data.loc[self.data.Position == -1.0].index, 
                 self.data.Short_SMA[self.data.Position == -1.0], 
                 'v', markersize=10, color='r', label='Sell Signal')
        
        ax1.set_title(f'{self.ticker} Strategy Analysis')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2: Portfolio Value vs Buy & Hold
        ax2 = plt.subplot(2, 1, 2)
        ax2.plot(self.data['Cumulative_Strategy'], label='Algo Strategy', color='blue')
        ax2.plot(self.data['Cumulative_Market'], label='Buy & Hold', color='grey', linestyle='--')
        ax2.set_title('Portfolio Performance ($10k Start)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

# ==========================================
# EXECUTION
# ==========================================
# Try 'BTC-USD' for Bitcoin or 'SPY' for Stocks
bot = MovingAverageBot('TSLA', start_date='2020-01-01', short_window=50, long_window=200)

bot.download_data()
bot.generate_signals()
bot.backtest()
bot.plot_results()