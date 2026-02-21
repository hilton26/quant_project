import numpy as np
import matplotlib.pyplot as plt

# Configuration
T = 1.0       # Total time (1 year)
N = 1000      # Number of steps
dt = T / N    # Time step size

# 1. Generate the "Increments" (dW)
# We scale the random numbers by sqrt(dt) because variance = dt implies std_dev = sqrt(dt)
dW = np.random.normal(0, np.sqrt(dt), N)

# 2. Accumulate them to get the Level (W)
# The Wiener process is just the cumulative sum of these random shocks
W = np.cumsum(dW)
W = np.insert(W, 0, 0) # Start at 0

# Plotting
time_axis = np.linspace(0, T, N+1)
plt.figure(figsize=(10, 4))
plt.plot(time_axis, W)
plt.title("A Realisation of a Wiener Process $W_t$", fontsize=14)
plt.xlabel(f"Time ($t$) over {T:.1f} year{'s' if T != 1 else ''}")
plt.ylabel("$W_t$")
plt.grid(True, alpha=0.5)
plt.show()