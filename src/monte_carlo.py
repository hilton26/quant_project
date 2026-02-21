import numpy as np
from scipy.stats import norm # Used for the probability math (Cumulative Distribution Function)

# ==========================================
# PART 1: The Analytic Approach (Black-Scholes)
# ==========================================

def calculate_black_scholes(S, K, T, r, sigma):
    """
    Calculates the theoretical price of a Call Option and its Delta.
    
    Terms:
    S     = Current Stock Price
    K     = Strike Price (The price we agree to buy at later)
    T     = Time to maturity (in years)
    r     = Risk-free interest rate (e.g., 0.05 for 5%)
    sigma = Volatility (Standard deviation of returns)
    """
    
    # The Black-Scholes formulas (d1 and d2)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calculate Call Price
    call_price = (S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    
    # Calculate Delta (The "Greek" measure of risk)
    # Delta tells us: If stock price moves $1, how much does the option move?
    delta = norm.cdf(d1)
    
    return call_price, delta

# ==========================================
# PART 2: The Simulation Approach (Monte Carlo)
# ==========================================

def run_monte_carlo(S, T, r, sigma, iterations=5):
    """
    Simulates random future price paths for a stock.
    This uses "Geometric Brownian Motion" - the standard model for stock movement.
    """
    print(f"\n--- Running Monte Carlo Simulation ({iterations} iterations) ---")
    
    dt = 1/252 # Time step (assuming 252 trading days in a year)
    days = int(T * 252) # Total days to simulate
    
    for i in range(iterations):
        price_path = [S]
        current_price = S
        
        for day in range(days):
            # Generate a random shock (Z) from a normal distribution
            # This represents the "Stochastic" (random) part of the market
            Z = np.random.normal(0, 1) 
            
            # The Formula for Geometric Brownian Motion:
            # New Price = Old Price * e^( (Drift) + (Random Shock) )
            drift = (r - 0.5 * sigma**2) * dt
            shock = sigma * np.sqrt(dt) * Z
            
            current_price = current_price * np.exp(drift + shock)
            price_path.append(current_price)
            
        final_price = price_path[-1]
        print(f"Simulation {i+1}: Final Price = ${final_price:.2f}")

# ==========================================
# EXECUTION
# ==========================================

# Parameters
current_stock_price = 100
strike_price = 105
time_to_expiry = 1    # 1 Year
risk_free_rate = 0.05 # 5%
volatility = 0.20     # 20% (Implies the stock swings somewhat moderately)

print(f"Input: Stock=${current_stock_price}, Strike=${strike_price}, Volatility={volatility*100}%")

# 1. Run Black-Scholes
price, delta = calculate_black_scholes(current_stock_price, strike_price, time_to_expiry, risk_free_rate, volatility)
print(f"\n--- Black-Scholes Results ---")
print(f"Theoretical Option Price: ${price:.2f}")
print(f"Option Delta: {delta:.4f}")
print(f"Interpreting Delta: If the stock goes up to $101, this option will gain approx ${delta:.2f}")

# 2. Run Monte Carlo
run_monte_carlo(current_stock_price, time_to_expiry, risk_free_rate, volatility)