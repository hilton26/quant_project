import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def bs_price(S, K, T, r, sigma):
    # Just a helper to calculate price for the plot
    # (Assuming we imported norm from scipy.stats)
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return (S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))

# Create a grid of Stock Prices and Times
S_vals = np.linspace(50, 150, 50)
T_vals = np.linspace(0.1, 1.0, 50) # Time from 0.1 to 1 year
S_grid, T_grid = np.meshgrid(S_vals, T_vals)

# Calculate Price at every point
# (Assuming Strike K=100, r=0.05, sigma=0.2)
Z_vals = bs_price(S_grid, 100, T_grid, 0.05, 0.2)

# 3D Surface Plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_grid, T_grid, Z_vals, cmap=cm.viridis, edgecolor='none')

ax.set_xlabel('Stock Price ($S$)')
ax.set_ylabel('Time to Maturity ($T$)')
ax.set_zlabel('Option Price ($V$)')
ax.set_title('Solution to Black-Scholes PDE (Option Value Surface)')
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()