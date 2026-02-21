import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==========================================
# 1. DEFINE THE FUNCTIONS
# ==========================================

def calculate_greeks(S, K, T, r, sigma):
    # Black-Scholes Components
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    # Delta (Speed)
    delta = norm.cdf(d1)
    
    # Gamma (Acceleration)
    # Note: We use norm.pdf (Probability Density), not cdf
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    return delta, gamma

# ==========================================
# 2. SETUP ANALYSIS
# ==========================================
K = 100       # Strike Price
r = 0.05      # Risk-free rate
sigma = 0.20  # Volatility
S_range = np.linspace(70, 130, 100) # Stock price moving from $70 to $130

# We will check Gamma at 3 different times:
# 1. Long term (1 Year left)
# 2. Short term (1 Month left)
# 3. Expiry imminent (1 Day left)
times = [1.0, 1/12, 1/252] 
labels = ['1 Year', '1 Month', '1 Day']
colors = ['green', 'blue', 'red']

# ==========================================
# 3. PLOTTING
# ==========================================
plt.figure(figsize=(12, 6))

for T, label, color in zip(times, labels, colors):
    gammas = []
    for S in S_range:
        _, g = calculate_greeks(S, K, T, r, sigma)
        gammas.append(g)
    
    plt.plot(S_range, gammas, label=f'Time to Expiry: {label}', color=color, linewidth=2)

plt.title('The "Gamma Explosion" Risk', fontsize=14)
plt.xlabel('Stock Price ($S$)', fontsize=12)
plt.ylabel('Gamma ($\Gamma$)', fontsize=12)
plt.axvline(x=K, color='black', linestyle=':', label='Strike Price ($100)')
plt.legend()
plt.grid(True, alpha=0.3)

# Annotate the danger zone
plt.annotate('Maximum Instability', xy=(100, 0.08), xytext=(110, 0.10),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()