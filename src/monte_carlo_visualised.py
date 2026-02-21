import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================
S = 100        # Starting Stock Price
T = 1          # Time to maturity (1 Year)
r = 0.05       # Risk-free interest rate (5%)
sigma = 0.20   # Volatility (20%)
iterations = 50 # Number of separate simulations to run
steps = 252    # Trading days in a year

def simulate_paths(S, T, r, sigma, steps, iterations):
    dt = T / steps
    # Create a blank array to hold all price paths
    # Shape: (steps + 1, iterations) -> Rows are days, Columns are different simulations
    paths = np.zeros((steps + 1, iterations))
    
    # Set the first row (Day 0) to the starting price for all simulations
    paths[0] = S
    
    # Loop through each time step
    for t in range(1, steps + 1):
        # Generate random shocks (Z) for ALL iterations at once (Vectorization)
        # This is much faster than using a 'for' loop for each simulation
        Z = np.random.normal(0, 1, iterations)
        
        # Geometric Brownian Motion Formula
        drift = (r - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt) * Z
        
        # Calculate new prices based on the previous day's prices
        paths[t] = paths[t-1] * np.exp(drift + shock)
        
    return paths

# ==========================================
# EXECUTION & PLOTTING
# ==========================================

print(f"Simulating {iterations} paths...")
price_paths = simulate_paths(S, T, r, sigma, steps, iterations)

# Setup the Plot
plt.figure(figsize=(10, 6))
plt.plot(price_paths)

# Formatting the Chart
plt.title(f'Monte Carlo Simulation: {iterations} Possible Futures', fontsize=14)
plt.xlabel('Trading Days', fontsize=12)
plt.ylabel('Stock Price ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Add a horizontal line for the starting price for reference
plt.axhline(y=S, color='black', linestyle=':', label='Start Price')
plt.legend()

# Show the plot
plt.show()