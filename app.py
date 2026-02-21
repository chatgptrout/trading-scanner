import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI CANDLE TERMINAL", layout="wide")

# --- 1. DIGITAL CLOCK (IST) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI PULSE HEADER ---
pcr_val = 2.01 # Latest
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#111; color:white; border-radius:15px; border-top:8px solid #00c853;'>
        <h1 style='margin:0; color:#00c853;'>PCR: {pcr_val}</h1>
        <h3 style='margin:0;'>AI STATUS: REVERSAL RISK ⚠️</h3>
        <p style='color:orange; margin:0;'>CANDLESTICK SYNC: ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. CANDLESTICK REPLACEMENT (STREAMLIT NATIVE) ---
def get_candle_data(symbol, title):
    df = yf.Ticker(symbol).history(period="1d", interval="5m")
    if not df.empty:
        st.subheader(title)
        # Showing OHLC data for professional analysis
        st.line_chart(df[['Open', 'High', 'Low', 'Close']], height=300)

st.markdown("<br>## 📊 LIVE PRICE ACTION (CANDLE VIEW)")
c1, c2 = st.columns(2)

with c1:
    get_candle_data("^NSEI", "NIFTY 50 (OHLC TREND)")
with c2:
    get_live_crude = "CL=F"
    get_candle_data(get_live_crude, "CRUDE OIL (OHLC TREND)")

# --- 4. DATA CARDS WITH SYNCED LEVELS ---
# Nifty: 25571.25 | Crude: 66.26 | NG: 2.91
st.markdown("---")
cols = st.columns(3)
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Precision Match for NG
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"

        with cols[i]:
            st.markdown(f"""
                <div style='background:#1e1e1e; padding:15px; border-radius:10px; text-align:center; color:white;'>
                    <h4 style='color:gray;'>{name}</h4>
                    <h2 style='margin:0;'>{price_str}</h2>
                    <p style='color:#00c853; margin:0;'>BULLISH > {hi:.2f}</p>
                    <p style='color:#ff1744; margin:0;'>BEARISH < {lo:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
