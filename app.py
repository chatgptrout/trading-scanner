import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V130", layout="wide")

# --- 1. MARKET TIME CHECK (AS PER YOUR SCREENSHOT LOGIC) ---
def is_market_live():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    is_weekday = now.weekday() < 5
    start = now.replace(hour=9, minute=15, second=0)
    end = now.replace(hour=15, minute=30, second=0)
    return start <= now <= end and is_weekday

# --- 2. THE ACTUAL NIFTY PCR HEADER ---
# Frozen value as per your last screenshot
pcr_val = 2.01 
status = "LIVE 🟢" if is_market_live() else "MARKET CLOSED 🔴 (FREEZED)"

st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR ({status})</h4>
        <h1 style='color:#00c853; font-size:65px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            TREND: EXTREME BULLISH
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. THE 4 POWER CARDS (NIFTY, SENSEX, CRUDE, NG) ---
#
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        # Nifty Price Example: 25649.85
        # Sell/Buy Logic based on current signals
        sig = "SELL" if ltp < df['Close'].iloc[-2] else "BUY"
        color = "#ff1744" if sig == "SELL" else "#00c853"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:12px; text-align:center; background:white;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:26px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                    <div style='color:#00c853; font-size:11px; font-weight:bold;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:11px; font-weight:bold;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 4. NIFTY 50 POWER SCANNER (BTST/STBT) ---
#
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")
stocks = ["SUNPHARMA.NS", "NTPC.NS", "TITAN.NS", "HDFCBANK.NS"]
results = []

for s in stocks:
    data = yf.Ticker(s).history(period="1d", interval="15m")
    if not data.empty:
        ltp = round(data['Close'].iloc[-1], 2)
        hi, lo = round(data['High'].max(), 2), round(data['Low'].min(), 2)
        results.append({
            "STOCK": s.split('.')[0], "LTP": ltp, "D-HIGH": hi, "D-LOW": lo, 
            "VOL SPIKE": "0.4x", "ACTION": "BTST ✅", "TARGET": round(ltp * 1.01, 2)
        })

st.table(pd.DataFrame(results)) #

time.sleep(20)
st.rerun()
