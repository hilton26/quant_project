print("$dS_t$ = r S_t dt + \sigma S_t dW_t$ represents the Geometric Brownian Motion SDE.")

import numpy as np
import matplotlib.pyplot as plt

# Configuration
T = 1.0       # Total time (1 year)
N = 1000      # Number of steps
dt = T / N    # Time step size

# 1. Generate the "Increments" (dW)
# We scale the random numbers by sqrt(dt) because variance = dt implies std_dev = sqrt(dt)
dW = np.random.normal(0, np.sqrt(dt), N)

# Parameters
mu = 0.1      # 10% Annual Drift
sigma = 0.2   # 20% Volatility
S0 = 100      # Start Price

# Simulation containers
S = np.zeros(N+1)
S[0] = S0

# Stepping through time (Euler-Maruyama Discretization)
for t in range(1, N+1):
    # This loop is literally the equation: dS = S * (mu*dt + sigma*dW)
    shock = dW[t-1] # The dW we generated earlier
    dS = S[t-1] * (mu * dt + sigma * shock)
    S[t] = S[t-1] + dS

time_axis = np.linspace(0, T, N+1)
plt.figure(figsize=(10, 4))
plt.plot(time_axis, S)
# plt.title(f"$dS_t$ = $\mu$ $S_t$ dt + $\sigma$ $S_t$ $dW_t$\n" \
#           f"Geometric Brownian Motion (Drift={mu}, Vol={sigma})")
plt.title(f"$dS_t$ = $\mu$ $S_t$ dt + $\sigma$ $S_t$ $dW_t$ \
    \nGeometric Brownian Motion with drift $\mu$ = {mu} and volatility ($\sigma$) = {sigma})")

plt.xlabel("Time")
plt.ylabel("Stock Price ($S_t$)")
plt.grid(True, alpha=0.5)
plt.show()