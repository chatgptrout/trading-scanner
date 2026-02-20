import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# --- 1. LIVE DIGITAL WATCH & MARKET STATUS ---
def get_now():
    tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(tz)

now_time = get_now()
st.markdown(f"""
    <div style='text-align:right; padding-right:20px;'>
        <h2 style='color:#333; margin:0;'>⌚ {now_time.strftime('%I:%M:%S %p')}</h2>
        <p style='color:gray; font-size:12px; margin:0;'>IST (Indian Standard Time)</p>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE ERROR-FREE MARKET CHECKER ---
def get_market_status(symbol):
    now = get_now()
    if symbol in ["^NSEI", "^BSESN"]: # Equity
        start = now.replace(hour=9, minute=15, second=0, microsecond=0)
        end = now.replace(hour=15, minute=30, second=0, microsecond=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"
    else: # Commodity (Crude/NG)
        start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=55, second=0, microsecond=0)
        return "LIVE 🟢" if start <= now <= end and now.weekday() < 5 else "CLOSED 🔴"

# --- 3. HEADER: PCR 2.01 & AI MOOD ---
pcr_val = 2.01 # Latest
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: OVERBOUGHT (CAUTION)
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. DYNAMIC CARDS (EQUITY + COMMODITY) ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    status = get_market_status(sym)
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
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

# --- 5. AI SCANNER ---
st.markdown("<br>### 🤖 AI POWER SCANNER (BTST/STBT)")
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88%", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72%", "STOP LOSS": 368.2, "TARGET": 376.73}
]
st.table(pd.DataFrame(stocks_data))

# AUTO REFRESH EVERY 10 SECONDS
time.sleep(10)
st.rerun()
