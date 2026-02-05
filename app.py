import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Santosh Free Scanner", layout="wide")
st.title("SANTOSH FREE SMART SCANNER")

# Crude Oil Feb Future (MCX) ka Yahoo symbol usually ye hota hai
# Note: Yahoo par commodity data thoda delay ho sakta hai
symbol = "CL=F" # Ye International Crude hai, MCX ke liye 'CRUDEOIL26FEB.F' try karein

st.sidebar.header("Market Watch")
market_type = st.sidebar.selectbox("Select Market", ["Crude Oil", "Nifty 50"])

if market_type == "Crude Oil":
    ticker_symbol = "CL=F"
    label = "CRUDE OIL (Global)"
else:
    ticker_symbol = "^NSEI"
    label = "NIFTY 50"

try:
    # Data fetch kar rahe hain
    with st.spinner('Fetching Live Data...'):
        data = yf.Ticker(ticker_symbol)
        # Fast info se current price nikalna
        current_price = data.fast_info['last_price']
        prev_close = data.fast_info['previous_close']
        change = current_price - prev_close
        
        # Display Price
        st.metric(label=label, value=f"{current_price:.2f}", delta=f"{change:.2f}")
        
        st.success("LIVE DATA CONNECTED (FREE)")
        st.info("Note: Yahoo Finance data 1-15 minute delay ho sakta hai.")

except Exception as e:
    st.error(f"System Error: {e}")
    st.info("Tip: Kabhi kabhi Yahoo server busy hota hai, 1 minute baad refresh karein.")
