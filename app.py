import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Advanced Trading Signals", layout="wide")

# Navigation Sidebar
st.sidebar.title("🚀 Strategy Mode")
app_mode = st.sidebar.radio("Select Category", ["Commodity", "Stocks", "Nifty/Sensex Strike"])

def get_advanced_signal(ticker):
    try:
        # Fetching 5 days of 15-minute data for better calculation
        data = yf.Ticker(ticker).history(period="5d", interval="15m")
        if data.empty: return "N/A", 0, "Wait"
        
        current_price = round(data['Close'].iloc[-1], 2)
        ema_20 = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        day_high = round(data['High'].iloc[-1], 2)
        day_low = round(data['Low'].iloc[-1], 2)

        # Strategy Logic
        if current_price > ema_20:
            signal = f"BULLISH ABOVE {ema_20}"
            status = "BUY"
            color = "green"
        else:
            signal = f"BEARISH BELOW {ema_20}"
            status = "SELL"
            color = "red"
        
        return current_price, signal, status, color
    except:
        return 0, "Error", "N/A", "white"

# --- PAGE 1: COMMODITY ---
if app_mode == "Commodity":
    st.header("🛢️ Advanced Commodity Signals")
    items = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    
    cols = st.columns(4)
    cols[0].write("**SCRIPT**")
    cols[1].write("**LTP**")
    cols[2].write("**STRATEGY LEVEL**")
    cols[3].write("**ACTION**")
    
    for name, sym in items.items():
        price, sig, stat, clr = get_advanced_signal(sym)
        c = st.columns(4)
        c[0].write(name)
        c[1].write(f"₹{price}")
        c[2].write(sig)
        if stat == "BUY": c[3].success(stat)
        else: c[3].error(stat)

# --- PAGE 2: STOCKS ---
elif app_mode == "Stocks":
    st.header("📈 Intraday Stock Scanner")
    stocks = {"RELIANCE": "RELIANCE.NS", "BHARAT FORGE": "BHARATFORG.NS", "TATA MOTORS": "TATAMOTORS.NS"}
    
    for name, sym in stocks.items():
        price, sig, stat, clr = get_advanced_signal(sym)
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 2])
            col1.subheader(name)
            col2.info(f"Signal: {sig}")
            if stat == "BUY": col3.button(f"PROFIT: {stat}", key=name, help="Trend is Positive")
            else: col3.button(f"RISK: {stat}", key=name)
        st.divider()

# --- PAGE 3: INDEX ---
elif app_mode == "Nifty/Sensex Strike":
    st.header("🎯 Index Reversal Levels")
    indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
    
    for name, sym in indices.items():
        price, sig, stat, clr = get_advanced_signal(sym)
        st.subheader(f"{name}: {price}")
        st.markdown(f"### Status: :{clr}[{sig}]")
        st.write("Suggested Strike: ATM CE if Buy, ATM PE if Sell")
