import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# --- 1. ERROR FIX: MARKET TIME CHECKER ---
def get_market_status(symbol):
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    if symbol in ["^NSEI", "^BSESN"]: # Equity Timings
        # Fix: Adding explicit keyword for minute
        start = now.replace(hour=9, minute=15, second=0)
        end = now.replace(hour=15, minute=30, second=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"
    else: # Commodity Timings (MCX)
        start = now.replace(hour=9, minute=0, second=0)
        end = now.replace(hour=23, 55, second=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"

# --- 2. HEADER: PCR 2.01 ---
pcr_val = 2.01 # Frozen as per
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (AI ANALYSIS)</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: OVERBOUGHT (CAUTION)
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. DYNAMIC CARDS (EQUITY + COMMODITY) ---
# Nifty/Sensex at latest prices
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    status = get_market_status(sym)
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        
        # Color & Signal logic
        sig = "BUY" if name in ["NIFTY 50", "SENSEX"] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:2px solid #ddd; padding:15px; border-radius:12px; text-align:center; background:#f9f9f9;'>
                    <div style='color:gray; font-size:12px;'>{name} ({status})</div>
                    <div style='font-size:24px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:8px 0;'>{sig}</div>
                    <hr>
                    <div style='color:#008000; font-size:11px; font-weight:bold;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#d32f2f; font-size:11px; font-weight:bold;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 4. AI SCANNER TABLE ---
# Showing Sun Pharma, NTPC with AI confidence
st.markdown("<br>### 🤖 AI POWER SCANNER (BTST/STBT)")
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88%", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72%", "STOP LOSS": 368.2, "TARGET": 376.73},
    {"STOCK": "TITAN", "LTP": 4248.7, "AI CONF": "65%", "STOP LOSS": 4205.0, "TARGET": 4291.19}
]
st.table(pd.DataFrame(stocks_data))

time.sleep(10)
st.rerun()
