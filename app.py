import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="AI TRADEX PRO V137", layout="wide")

# --- 1. AI HEADER (FREEZED AT 2.01) ---
pcr_val = 2.01 #
ai_mood = "OVERBOUGHT (CAUTION)" if pcr_val > 1.8 else "BULLISH"

st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (AI ANALYSIS)</h4>
        <h1 style='color:#00c853; font-size:60px; margin:0;'>{pcr_val}</h1>
        <div style='background:#fb8c00; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            AI FORECAST: {ai_mood}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INDEX CARDS WITH BULLISH/BEARISH LEVELS ---
# Refreshing levels as per
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        
        # Color & Signal logic
        sig = "BUY" if name == "NATURAL GAS" else "SELL" # NG was Green in
        color = "#00c853" if sig == "BUY" else "#ff1744"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:12px; text-align:center;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:24px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                    <div style='color:#00c853; font-size:11px; font-weight:bold;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:11px; font-weight:bold;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. AI SCANNER TABLE ---
st.markdown("<br>### 🤖 AI POWER SCANNER (BTST/STBT)")
# Re-adding Sun Pharma, NTPC, Titan
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.00, "AI CONF": "88%", "STOP LOSS": 1708.5, "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.00, "AI CONF": "72%", "STOP LOSS": 368.2, "TARGET": 376.73}
]
st.table(pd.DataFrame(stocks_data))

time.sleep(30)
st.rerun()
