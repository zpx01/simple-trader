import streamlit as st
from streamlit.logger import get_logger

# Import your trading strategy
from trader import SimpleTrader
# Library to pull stock data
import yfinance as yf

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Simple Trading Strategy",
        page_icon="👋",
    )
    st.write("# Simple Trading Strategy")
    ticker = st.text_input(label='Enter a stock ticker')
    if ticker:
        data = yf.download(f"SPY {ticker}", 
                        start="2017-01-01", 
                        end="2024-04-01", 
                        group_by="ticker")
        
        st.write("### Data from stock")
        st.dataframe(data)
        trader = SimpleTrader(data, ticker)
        # Call trading strategy
        signals = trader.moving_average_crossover()
        # Plot signals
        st.write('## Signals Plot')
        trader.plot_signals(signals)
        # Calculate PnL of strategy
        returns = trader.calculate_returns(signals)
        st.write(f"Total Returns (%): {returns}")


if __name__ == "__main__":
    run()
