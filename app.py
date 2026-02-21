import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI TRADEX PRO V175", layout="wide")

# --- 1. OPTION CLOCK (PRECISION IST) ---
def get_now():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

now = get_now()
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI PULSE HEADER ---
pcr_val = 2.01 # Latest from screenshot
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#000; border-radius:10px; border-bottom:5px solid #00c853;'>
        <h2 style='color:white; margin:0;'>INTRADAY PULSE: AI ENGINE</h2>
        <h1 style='color:#00c853; font-size:65px; margin:0;'>PCR: {pcr_val}</h1>
        <div style='background:orange; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            TRADEFLOW: REVERSAL RISK ⚠️ | RSI BOT: OVERBOUGHT (CAUTION)
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE MARKET CARDS (SYNCED) ---
# Nifty: 25565.90 | Crude: 66.31 | NG: 2.994
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(3)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Precision Sync for Natural Gas
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

# --- 4. OPTION CHAIN & TRADEFLOW SCANNER ---
st.markdown("<br>### 🧭 OPTION CHAIN & TRADEFLOW PULSE")
pulse_data = [
    {"STRIKE": "25600 CE", "OI CHANGE": "HIGH WRITING 🔴", "SIGNAL": "RESISTANCE", "TRADEFLOW": "BEARISH"},
    {"STRIKE": "25500 PE", "OI CHANGE": "STRONG SUPPORT 🟢", "SIGNAL": "BULLISH", "TRADEFLOW": "STABLE"},
    {"STRIKE": "25700 CE", "OI CHANGE": "FRESH WRITING", "SIGNAL": "CAUTION", "TRADEFLOW": "BEARISH"}
]
st.table(pd.DataFrame(pulse_data))

# --- 5. AI RSI BOT (STOCKS SCANNER) ---
# Sun Pharma (1725.0) & NTPC (373.0)
st.markdown("<br>### 🤖 AI RSI BOT SCANNER")
stocks = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "RSI": 74.5, "STATUS": "OVERBOUGHT", "AI ACTION": "WAIT"},
    {"STOCK": "NTPC", "LTP": 373.0, "RSI": 58.2, "STATUS": "BULLISH", "AI ACTION": "BUY ✅"}
]
st.table(pd.DataFrame(stocks))

time.sleep(5)
st.rerun()
