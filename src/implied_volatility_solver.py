import numpy as np
from scipy.stats import norm

# ==========================================
# 1. THE BLACK-SCHOLES FUNCTIONS
# ==========================================
def bs_price(S, K, T, r, sigma, type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if type == 'call':
        return (S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    else: # put
        return (K * np.exp(-r * T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))

def bs_vega(S, K, T, r, sigma):
    # Vega is the derivative of Price with respect to Volatility
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

# ==========================================
# 2. THE NEWTON-RAPHSON SOLVER
# ==========================================
def find_implied_volatility(target_price, S, K, T, r, type='call'):
    """
    Finds the volatility that makes the Black-Scholes price equal to the Target Price.
    """
    MAX_ITERATIONS = 100
    PRECISION = 1e-5
    
    sigma = 0.5 # Initial guess (50%)
    
    for i in range(MAX_ITERATIONS):
        price = bs_price(S, K, T, r, sigma, type)
        vega = bs_vega(S, K, T, r, sigma)
        
        diff = target_price - price  # How far off are we?
        
        if abs(diff) < PRECISION:
            return sigma
        
        # Newton-Raphson Step:
        # New Guess = Old Guess + (Error / Gradient)
        sigma = sigma + diff / vega
        
    return sigma # Return best guess if we hit max iterations

# ==========================================
# 3. TEST IT
# ==========================================
S = 100
K = 100
T = 1
r = 0.05

# Let's say the market price is $12.00 (But we don't know the volatility yet)
market_price = 12.00

implied_vol = find_implied_volatility(market_price, S, K, T, r, 'call')

print(f"Market Price: ${market_price}")
print(f"The Implied Volatility is: {implied_vol*100:.2f}%")