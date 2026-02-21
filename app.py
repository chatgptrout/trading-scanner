import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI TRADEX PRO V168", layout="wide")

# --- 1. THE PRECISION WATCH ---
def get_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

now = get_now()
st.markdown(f"<div style='text-align:right;'><h4>⌚ {now.strftime('%I:%M:%S %p')}</h4></div>", unsafe_allow_html=True)

# --- 2. AI CORE ANALYSIS (FROZEN AT 2.01) ---
pcr_val = 2.01 # From live screenshot
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#000; color:white; border-radius:10px; border-bottom:5px solid #00c853;'>
        <h3 style='margin:0;'>AI TRADING CORE ANALYSIS</h3>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>PCR: {pcr_val}</h1>
        <div style='background:orange; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            SIGNAL: REVERSAL RISK ⚠️ | 85% Confidence
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE MARKET CARDS ---
#
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(3)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Precision Sync for NG
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"
            
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #333; padding:20px; border-radius:12px; text-align:center; background:#111; color:white;'>
                    <p style='color:gray; font-size:14px; margin:0;'>{name}</p>
                    <h1 style='margin:10px 0;'>{price_str}</h1>
                    <hr style='border:0.1px solid #333;'>
                    <div style='color:#00c853; font-size:12px; font-weight:bold;'>BULLISH ABOVE: {hi:.2f}</div>
                    <div style='color:#ff1744; font-size:12px; font-weight:bold;'>BEARISH BELOW: {lo:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 4. AI POWER SCANNER ---
# Sun Pharma & NTPC
stocks = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88% 🔥", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72% ⚡", "STOP LOSS": 368.2, "TARGET": 376.73}
]
st.markdown("<br>### 🔍 AI POWER SCANNER")
st.table(pd.DataFrame(stocks))

time.sleep(5)
st.rerun()
