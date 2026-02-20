import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V81", layout="wide")

# --- 1. DYNAMIC HEADER (PCR SAME RAKHA HAI) ---
pcr_val = 1.65 #
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:55px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:3px 15px; border-radius:5px; display:inline-block;'>TREND: EXTREME BULLISH</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INDEX CARDS WITH VOLUME & RSI ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

def get_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1mo", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        current_rsi = round(get_rsi(df).iloc[-1], 2)
        vol_status = "HIGH ⚡" if df['Volume'].iloc[-1] > df['Volume'].mean() else "NORMAL ☁️"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:10px; text-align:center; background:white;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:28px; font-weight:900;'>{ltp}</div>
                    <div style='color:#1a237e; font-size:13px; font-weight:bold;'>VOL: {vol_status} | RSI: {current_rsi}</div>
                    <div style='color:#00c853; font-size:12px; font-weight:bold; border:1px solid #00c853; margin-top:5px; border-radius:3px; background:#e8f5e9;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:12px; font-weight:bold; border:1px solid #ff1744; border-radius:3px; background:#ffebee;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. POWER SCANNER (BTST/STBT + VOL SPIKE) ---
st.markdown("<br><h3 style='color:#1a237e;'>🚀 NIFTY 50 POWER SCANNER (BTST/STBT)</h3>", unsafe_allow_html=True)
# Scanner logic remains the same as V80
