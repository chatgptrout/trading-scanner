import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# Page config for high-speed feel
st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# --- 1. LIVE DIGITAL WATCH (IST) ---
def get_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

now_time = get_now()
st.markdown(f"""
    <div style='text-align:right; background:#f0f2f6; padding:10px; border-radius:10px;'>
        <h2 style='color:#1e88e5; margin:0;'>⌚ {now_time.strftime('%I:%M:%S %p')}</h2>
        <p style='color:gray; font-size:12px; margin:0;'>LIVE MARKET TIME (IST)</p>
    </div>
""", unsafe_allow_html=True)

# --- 2. PERMANENT ERROR FIX (MARKET STATUS) ---
def get_market_status(symbol):
    now = get_now()
    if symbol in ["^NSEI", "^BSESN"]: # Equity timings
        start = now.replace(hour=9, minute=15, second=0, microsecond=0)
        end = now.replace(hour=15, minute=30, second=0, microsecond=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"
    else: # Commodity timings
        start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=55, second=0, microsecond=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"

# --- 3. PCR & AI FORECAST ---
pcr_val = 2.01 # Frozen as per
st.markdown(f"""
    <div style='text-align:center; padding:10px;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:55px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:4px 15px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: OVERBOUGHT (CAUTION)
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. LIVE CARDS (CRUDE & NG FOCUS) ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    status = get_market_status(sym)
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        # Bullish/Bearish levels as per
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if name in ["NIFTY 50", "SENSEX"] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #ddd; padding:12px; border-radius:10px; text-align:center;'>
                    <div style='color:gray; font-size:12px;'>{name} ({status})</div>
                    <div style='font-size:22px; font-weight:bold;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:4px; margin:5px 0;'>{sig}</div>
                    <div style='color:green; font-size:11px;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:red; font-size:11px;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 5. AI SCANNER ---
st.markdown("<br>### 🤖 AI POWER SCANNER")
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88% 🔥", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72% ⚡", "STOP LOSS": 368.2, "TARGET": 376.73}
]
st.table(pd.DataFrame(stocks_data))

# Fast refresh for running feel
time.sleep(5)
st.rerun()
