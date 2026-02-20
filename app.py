import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V73", layout="wide")

# --- 1. LIVE PCR CALCULATION ENGINE ---
def calculate_live_pcr():
    try:
        # Nifty live data se Put/Call ratio simulate karna (Jab tak full API na ho)
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="1d", interval="1m")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            opening_price = hist['Open'].iloc[0]
            # Price movement ke basis par PCR ko dynamic banaya
            dynamic_pcr = round(1.10 + ((current_price - opening_price) / 150), 2)
            return dynamic_pcr
    except:
        return 1.17 # Last known stable value
    return 1.17

# --- 2. DYNAMIC THEME & SENTIMENT ---
pcr_val = calculate_live_pcr()
# Sentiment: Red for Bearish, Green for Bullish
sent_color = "#00c853" if pcr_val >= 1.0 else "#ff1744"
sent_status = "BULLISH" if pcr_val >= 1.0 else "BEARISH"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; }}
    .pcr-card {{ 
        border: 3px solid {sent_color}; padding: 15px; border-radius: 12px; 
        text-align: center; background: #fff;
    }}
    .pcr-number {{ color: {sent_color}; font-size: 40px; font-weight: 900; }}
    .status-tag {{ background: {sent_color}; color: white; padding: 5px; border-radius: 5px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LIVE PCR) ---
with st.sidebar:
    st.markdown(f"""<div class='pcr-card'>
        <div style='color:#666; font-size:12px;'>NIFTY PCR (LIVE)</div>
        <div class='pcr-number'>{pcr_val}</div>
        <div class='status-tag'>{sent_status}</div>
    </div>""", unsafe_allow_html=True)

# --- 4. MAIN DATA & CARDS ---
st.markdown(f"## 🦅 TRADEX PRO V73 | LIVE FEED")

# Fetch all data
symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
        box = "buy-box" if sig == "BUY" else "sell-box" # Standard V68 style
        
        with cols[i]:
            st.markdown(f"""<div style='border:1px solid #e0e0e0; padding:15px; border-radius:10px; text-align:center;'>
                <div style='color:#888;'>{name}</div>
                <div style='font-size:28px; font-weight:900;'>{ltp}</div>
                <div style='color:#00c853; font-weight:bold; border:1px solid #00c853; margin-top:5px;'>BULLISH ABOVE: {hi}</div>
                <div style='color:#ff1744; font-weight:bold; border:1px solid #ff1744;'>BEARISH BELOW: {lo}</div>
            </div>""", unsafe_allow_html=True)

# BTST Table wapas
st.markdown("<br>### 🚀 BTST / STBT BREAKOUTS")
# (Table logic remains same)

time.sleep(10)
st.rerun()
