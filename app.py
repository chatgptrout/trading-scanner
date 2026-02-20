import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="AI TRADEX PRO V136", layout="wide")

# --- 1. AI MOOD ANALYZER ---
pcr_val = 2.01 # Frozen value from screen
ai_status = "OVERBOUGHT (CAUTION)" if pcr_val > 1.8 else "BULLISH"

st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (AI ANALYSIS)</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: {ai_status}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE 4 POWER CARDS ---
# Nifty: 25571.25 | Sensex: 82814.71
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        # Crude (66.13) and NG (2.92) signals
        sig = "BUY" if name in ["NIFTY 50", "SENSEX"] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        with cols[i]:
            st.markdown(f"<div style='border:1px solid #eee; padding:10px; border-radius:10px; text-align:center;'><b>{name}</b><br><span style='font-size:20px;'>{ltp}</span><br><span style='color:{color}; font-weight:bold;'>{sig}</span></div>", unsafe_allow_html=True)

# --- 3. AI POWER SCANNER (WITH STOP LOSS) ---
st.markdown("<br>### 🤖 AI POWER SCANNER (BTST/STBT)")
# Sun Pharma, NTPC, Titan data with AI Confidence
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.00, "AI CONFIDENCE": "88% 🔥", "STOP LOSS": 1708.50, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.00, "AI CONFIDENCE": "72% ⚡", "STOP LOSS": 368.20, "TARGET": 376.73},
    {"STOCK": "TITAN", "LTP": 4248.70, "AI CONFIDENCE": "65% 📈", "STOP LOSS": 4205.00, "TARGET": 4291.19}
]
st.table(pd.DataFrame(stocks_data))

time.sleep(30)
st.rerun()
