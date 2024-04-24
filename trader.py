import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class SimpleTrader:
    def __init__(self, df, ticker):
        """
        Args:
            df - dataframe object containing your stock data
            ticker - string with the stock ticker you want to analyze
        """
        self.df = df
        self.ticker = ticker
    
    def moving_average_crossover(self, short_window=10, long_window=50):
        """
        Moving Average Crossover Strategy:

        This strategy involves two moving averages of the stock price: a short-term moving average (e.g., 10 days) and a long-term moving average (e.g., 50 days). The basic idea is:

        - Buy signal: When the short-term moving average crosses above the long-term moving average.
        - Sell signal: When the short-term moving average crosses below the long-term moving average.
        """
        # Calculate moving averages
        signals = pd.DataFrame(index=self.df[self.ticker]['Close'].index)
        signals['signal'] = 0.0

        # TODO: Calculate the short_mavg and long_mavg using pandas (try https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)

        signals['short_mavg'] = ...
        signals['long_mavg'] = ...
        
        # Generate signals
        # Signals will be either 1 (buy) or 0 (sell)
        # Fill out the condition in np.where(condition, 1.0, 0.0) based on the short_mavg and long_mavg
        signals['signal'][short_window:] = np.where(..., 1.0, 0.0)   
        
        # Determine when the trading signal changes
        signals['positions'] = signals['signal'].diff()
        
        return signals
    
    def plot_signals(self, signals):
        # Plot the prices and buy and sell signals from moving averages
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(self.df[self.ticker]['Close'], label='Closing Price', color='blue')
        ax.plot(signals['short_mavg'], label='10-Day Moving Average', color='red', linestyle='--')
        ax.plot(signals['long_mavg'], label='50-Day Moving Average', color='black', linestyle='--')

        ax.plot(signals.loc[signals.positions == 1.0].index, 
                 signals.short_mavg[signals.positions == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')

        ax.plot(signals.loc[signals.positions == -1.0].index, 
                 signals.short_mavg[signals.positions == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')

        plt.title(f'{self.ticker} Stock Price and Moving Averages')
        plt.legend()
        
        # Render figure on streamlit app
        st.pyplot(fig)
    
    def calculate_returns(self, signals, num_shares=10):
        initial_investment = self.df[self.ticker]['Close'].iloc[0] * num_shares
        signals['holdings'] = self.df[self.ticker]['Close'] * signals['positions'].cumsum()

        # Calculate the cash position by adjusting for changes in position, considering the initial investment
        signals['cash'] = initial_investment + (signals['positions'].shift(1) * self.df[self.ticker]['Close']).cumsum().fillna(0)

        # Total portfolio value
        signals['total'] = signals['holdings'] + signals['cash']

        # TODO: Profit and Loss (PnL) = percentage difference between the final total value and the initial investment. Hint: Use .iloc[-1] to get the final total value
        pnl = ...  # Multiply by 100 at the end to get PnL as a percentage
        return pnl



    
