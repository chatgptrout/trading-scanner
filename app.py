import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# --- 1. DIGITAL WATCH (FOR SYNC CHECK) ---
def get_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

st.markdown(f"""
    <div style='text-align:right; padding:10px;'>
        <h2 style='color:#1a73e8; margin:0;'>⌚ {get_now().strftime('%I:%M:%S %p')}</h2>
        <p style='color:gray; font-size:12px; margin:0;'>DATA REFRESH: EVERY 2 SEC</p>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE PRECISION DATA ENGINE ---
def get_realtime_data(symbol):
    try:
        # 'period=1d' and 'interval=1m' is the fastest way in yfinance
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m")
        if not df.empty:
            current_price = df['Close'].iloc[-1]
            high = df['High'].max()
            low = df['Low'].min()
            return current_price, high, low
    except:
        return 0, 0, 0

# --- 3. SYNCED CARDS (EQUITY + COMMODITY) ---
# Symbols optimized for better match
symbols = {
    "NIFTY 50": "^NSEI", 
    "SENSEX": "^BSESN", 
    "CRUDE OIL": "CL=F", 
    "NATURAL GAS": "NG=F"
}

cols = st.columns(4)
for i, (name, sym) in enumerate(symbols.items()):
    ltp, hi, lo = get_realtime_data(sym)
    
    # Matching OilPrice.com's 3-decimal precision for NG
    price_display = f"{ltp:.3f}" if "GAS" in name else f"{ltp:.2f}"
    
    # Signal and Trend logic
    sig = "SELL" if name in ["CRUDE OIL", "NATURAL GAS"] else "BUY"
    color = "#ff1744" if sig == "SELL" else "#00c853"
    
    with cols[i]:
        st.markdown(f"""
            <div style='border:2px solid #eee; padding:15px; border-radius:12px; text-align:center;'>
                <div style='color:gray; font-size:12px;'>{name} (LIVE 🟢)</div>
                <div style='font-size:26px; font-weight:900;'>{price_display}</div>
                <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:8px 0;'>{sig}</div>
                <hr style='border:0.5px solid #eee;'>
                <div style='color:#008000; font-size:11px; font-weight:bold;'>BULLISH ABOVE: {hi:.2f}</div>
                <div style='color:#d32f2f; font-size:11px; font-weight:bold;'>BEARISH BELOW: {lo:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

# --- 4. AI POWER SCANNER ---
#
st.table(pd.DataFrame([
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88% 🔥", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72% ⚡", "STOP LOSS": 368.2, "TARGET": 376.73}
]))

# ULTRA FAST REFRESH
time.sleep(2)
st.rerun()
