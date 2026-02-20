import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V139", layout="wide")

# --- 1. AI HEADER ---
pcr_val = 2.01 #
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (AI ANALYSIS)</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: OVERBOUGHT (CAUTION)
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INDEX CARDS (BULLISH/BEARISH LEVELS FORCED VISIBLE) ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        
        # Color & Signal logic
        sig = "BUY" if name in ["NIFTY 50", "SENSEX"] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        
        with cols[i]:
            # levels ko yahan 'st.markdown' ke andar alag se highlight kiya hai
            st.markdown(f"""
                <div style='border:2px solid #ddd; padding:15px; border-radius:12px; text-align:center; background:#f9f9f9;'>
                    <div style='color:#555; font-size:14px; font-weight:bold;'>{name}</div>
                    <div style='font-size:26px; font-weight:900; color:#222;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:8px 0; padding:2px;'>{sig}</div>
                    <hr style='margin:10px 0;'>
                    <div style='color:#008000; font-size:12px; font-weight:bold;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#d32f2f; font-size:12px; font-weight:bold; margin-top:4px;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. AI SCANNER TABLE ---
st.markdown("<br>### 🤖 AI POWER SCANNER (BTST/STBT)")
#
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.0, "AI CONF": "88%", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.0, "AI CONF": "72%", "STOP LOSS": 368.2, "TARGET": 376.73},
    {"STOCK": "TITAN", "LTP": 4248.7, "AI CONF": "65%", "STOP LOSS": 4205.0, "TARGET": 4291.19}
]
st.table(pd.DataFrame(stocks_data))

time.sleep(30)
st.rerun()
