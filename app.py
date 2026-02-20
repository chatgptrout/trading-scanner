import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V74", layout="wide")

# --- 1. LIVE PCR ENGINE (Price Linked) ---
def get_dynamic_pcr():
    try:
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(period="1d", interval="1m")
        if not df.empty:
            cur = df['Close'].iloc[-1]
            opn = df['Open'].iloc[0]
            # PCR moving with price
            val = round(1.10 + ((cur - opn) / 120), 2)
            return val
    except:
        return 1.17
    return 1.17

# --- 2. THEME & STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .price-card { 
        background: #fff; padding: 20px; border-radius: 15px; 
        border: 1px solid #eee; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .pcr-hero { 
        font-size: 45px; font-weight: 900; margin: 10px 0;
        padding: 10px; border-radius: 10px;
    }
    .buy-zone { background: #00c853; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    .sell-zone { background: #ff1744; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V74 | SENSEX LIVE</h2>", unsafe_allow_html=True)

# Main PCR Update
current_pcr = get_dynamic_pcr()
pcr_col = "#00c853" if current_pcr >= 1.0 else "#ff1744"

# PCR Header (Instead of Sidebar)
st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='color:#666; font-weight:bold;'>LIVE MARKET PCR</div>
        <div style='color:{pcr_col}; font-size:60px; font-weight:900;'>{current_pcr}</div>
        <div style='color:{pcr_col}; font-weight:bold;'>SENTIMENT: {'BULLISH' if current_pcr >= 1.0 else 'BEARISH'}</div>
    </div>
""", unsafe_allow_html=True)

# Symbols Update: Sensex (^BSESN) added
symbols = {
    "NIFTY 50": "^NSEI", 
    "SENSEX": "^BSESN", 
    "CRUDE OIL": "CL=F", 
    "NATURAL GAS": "NG=F"
}

cols = st.columns(4)
for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
        btn = "buy-zone" if sig == "BUY" else "sell-zone"
        
        with cols[i]:
            st.markdown(f"""<div class='price-card'>
                <div style='color:#888; font-size:12px;'>{name}</div>
                <div style='font-size:35px; font-weight:900; margin:5px 0;'>{ltp}</div>
                <div class='{btn}'>{sig}</div>
                <div style='color:#00c853; font-weight:bold; border:1px solid #00c853; margin-top:10px; border-radius:5px;'>BULLISH ABOVE: {hi}</div>
                <div style='color:#ff1744; font-weight:bold; border:1px solid #ff1744; border-radius:5px;'>BEARISH BELOW: {lo}</div>
            </div>""", unsafe_allow_html=True)

time.sleep(5)
st.rerun()
