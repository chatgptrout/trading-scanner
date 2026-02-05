import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Santosh Auto-Scanner", layout="wide")
st.title("SANTOSH AUTOMATIC LIVE SCANNER")

# 1. Automatic Refresh Logic (Har 30 second mein reload hoga)
# Streamlit mein auto-refresh ke liye hum ye simple trick use kar rahe hain
if "count" not in st.session_state:
    st.session_state.count = 0

# 2. Watchlist (Aap yahan aur bhi stocks add kar sakte hain)
watchlist = {
    'NIFTY 50': '^NSEI',
    'BANK NIFTY': '^NSEBANK',
    'RELIANCE': 'RELIANCE.NS',
    'CRUDE OIL': 'CL=F',
    'TATA MOTORS': 'TATAMOTORS.NS'
}

# Layout: 3 Columns banate hain taaki sab ek saath dikhe
cols = st.columns(3)

for i, (name, ticker) in enumerate(watchlist.items()):
    with cols[i % 3]:
        try:
            data = yf.Ticker(ticker)
            info = data.fast_info
            price = info['last_price']
            change = price - info['previous_close']
            
            # Displaying Metric
            st.metric(label=name, value=f"{price:.2f}", delta=f"{change:.2f}")
        except:
            st.error(f"Error loading {name}")

# Auto-refresh mechanism
time.sleep(30)
st.rerun()
