import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Santosh Stock Tracker", layout="wide")
st.title("SANTOSH SMART SCANNER")

# Sidebar for Stock Selection
st.sidebar.header("Select What to Watch")
option = st.sidebar.selectbox(
    'Instrument',
    ('NIFTY 50', 'BANK NIFTY', 'RELIANCE', 'TATA MOTORS', 'CRUDE OIL')
)

# Mapping Symbols for Yahoo Finance
symbols = {
    'NIFTY 50': '^NSEI',
    'BANK NIFTY': '^NSEBANK',
    'RELIANCE': 'RELIANCE.NS',
    'TATA MOTORS': 'TATAMOTORS.NS',
    'CRUDE OIL': 'CL=F'
}

ticker = symbols[option]

try:
    data = yf.Ticker(ticker)
    price = data.fast_info['last_price']
    prev_close = data.fast_info['previous_close']
    change = price - prev_close
    percent_change = (change / prev_close) * 100

    # Display results
    st.metric(label=option, value=f"{price:.2f}", delta=f"{change:.2f} ({percent_change:.2f}%)")
    st.success(f"LIVE: {option} matched successfully!")

except Exception as e:
    st.error(f"Error fetching {option}: {e}")
