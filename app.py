import streamlit as st
import yfinance as yf

# Page Configuration
st.set_page_config(page_title="My Multi-App Trader", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🚀 Navigation")
app_mode = st.sidebar.radio("Select Dashboard", ["Commodity", "Stocks", "Nifty/Sensex Strike"])

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return 0, 0
        return round(df['Close'].iloc[-1], 2), round(df['Close'].iloc[-2], 2)
    except:
        return 0, 0

if app_mode == "Commodity":
    st.header("🛢️ Commodity Live Signals")
    items = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    for name, sym in items.items():
        curr, prev = get_data(sym)
        c1, c2, c3 = st.columns(3)
        c1.subheader(name)
        c2.metric("Price", curr, f"{round(curr-prev, 2)}")
        if curr > prev: c3.success(f"🟢 BULLISH ABOVE {prev}")
        else: c3.error(f"🔴 BEARISH BELOW {prev}")

elif app_mode == "Stocks":
    st.header("📈 Stock Watchlist")
    stocks = {"RELIANCE": "RELIANCE.NS", "BHARAT FORGE": "BHARATFORG.NS"}
    for name, sym in stocks.items():
        curr, prev = get_data(sym)
        c1, c2, c3 = st.columns([2, 2, 4])
        c1.write(f"**{name}**")
        c2.write(f"₹{curr}")
        c3.info("BULLISH" if curr > prev else "BEARISH")

elif app_mode == "Nifty/Sensex Strike":
    st.header("🎯 Index Levels")
    indices = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN"}
    for name, sym in indices.items():
        curr, prev = get_data(sym)
        st.subheader(f"{name}: {curr}")
        st.write(f"Trend: {'Upward' if curr > prev else 'Downward'}")
