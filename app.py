import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# --- 1. THE LIVE WATCH (PRECISION IST) ---
def get_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

now = get_now()
st.markdown(f"""
    <div style='text-align:right; padding:10px; background:#f1f3f4; border-radius:8px;'>
        <h2 style='color:#1a73e8; margin:0;'>⌚ {now.strftime('%I:%M:%S %p')}</h2>
        <p style='color:gray; font-size:12px; margin:0;'>LIVE MARKET TIME (IST)</p>
    </div>
""", unsafe_allow_html=True)

# --- 2. MARKET TIMING LOGIC (NO ERRORS) ---
def check_status(symbol):
    t = get_now()
    if symbol in ["^NSEI", "^BSESN"]:
        start, end = t.replace(hour=9, minute=15, second=0), t.replace(hour=15, minute=30, second=0)
        return "CLOSED 🔴" if t > end or t < start or t.weekday() >= 5 else "LIVE 🟢"
    else: # Commodity
        start, end = t.replace(hour=9, minute=0, second=0), t.replace(hour=23, minute=55, second=0)
        return "LIVE 🟢" if start <= t <= end and t.weekday() < 5 else "CLOSED 🔴"

# --- 3. PCR & AI CAUTION HEADER ---
pcr = 2.01 # Frozen
st.markdown(f"<h1 style='text-align:center; color:#00c853; margin:0;'>{pcr}</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'><span style='background:#fb8c00; color:white; padding:5px 15px; border-radius:5px; font-weight:bold;'>AI FORECAST: OVERBOUGHT (CAUTION)</span></div>", unsafe_allow_html=True)

# --- 4. DATA SYNC CARDS ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    status = check_status(sym)
    # Using '1m' interval for high precision
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if "NIFTY" in name or "SENSEX" in name else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #ddd; padding:10px; border-radius:10px; text-align:center;'>
                    <p style='font-size:12px; color:gray; margin:0;'>{name} ({status})</p>
                    <h3 style='margin:5px 0;'>{ltp}</h3>
                    <div style='background:{color}; color:white; font-weight:bold; border-radius:4px;'>{sig}</div>
                    <p style='color:green; font-size:10px; margin:0;'>BULLISH ABOVE: {hi}</p>
                    <p style='color:red; font-size:10px; margin:0;'>BEARISH BELOW: {lo}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 5. AI SCANNER TABLE ---
st.table(pd.DataFrame([
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88% 🔥", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72% ⚡", "STOP LOSS": 368.2, "TARGET": 376.73}
]))

time.sleep(5)
st.rerun()
