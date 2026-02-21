# Quant Finance Starter: Monte Carlo & Black-Scholes

This project is a Python-based introduction to Quantitative Finance concepts. It explores two foundational models used in financial engineering to price derivatives and simulate market behavior.

## 📊 Overview

The script (`monte_carlo.py`) performs two main tasks:
1.  **Black-Scholes Pricing:** Analytically calculates the fair value of a Call Option and its Delta (risk sensitivity).
2.  **Monte Carlo Simulation:** Uses Geometric Brownian Motion to simulate 50 random future price paths for a stock, visualizing the concept of stochastic processes.

## 🛠️ Technologies Used

* **Python 3.x**
* **NumPy:** For vectorization and random number generation.
* **SciPy:** For statistical functions (Cumulative Distribution Function).
* **Matplotlib:** For visualizing the "spaghetti plot" of price paths.

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/hilton26/quant-finance-learning.git](https://github.com/hilton26/quant-finance-learning.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install numpy scipy matplotlib
    ```
3.  **Run the script:**
    ```bash
    python monte_carlo.py
    ```

## 📉 Key Concepts

* **Delta ($\Delta$):** Represents the rate of change between the option's price and a $1 change in the underlying asset's price.
* **Stochastic Process:** The mathematical framework used to model the random behavior of assets over time.

---
*Created as part of my journey into Quantitative Finance.*


# 📈 Action Trading Bot (Aggressive Strategy)

This project is a Python-based algorithmic trading bot designed for **aggressive trend following**. Unlike standard conservative bots, this script prioritizes speed and entry volume over safety.

## ⚡ Strategy Logic
This bot uses a "Scalper" mentality:
* **Fast Reaction:** Uses a **10-day** Moving Average (vs. the standard 50) to catch trends immediately.
* **High Risk Tolerance:** Buys even when the asset is "Overbought" (RSI up to **80**), assuming strong momentum will continue.
* **Momentum Confirmation:** Uses MACD to confirm the trend direction.

## 🛠 Dependencies
* `yfinance` (Data feed)
* `pandas` & `numpy` (Calculation engine)
* `matplotlib` (Visualization dashboard)

## 🚀 How to Run
1.  Ensure you have the libraries installed:
    ```bash
    pip install yfinance pandas numpy matplotlib
    ```
2.  Run the script:
    ```bash
    python action_bot.py
    ```
3.  The dashboard will pop up showing **Price**, **MACD**, and **RSI**.