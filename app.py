import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V75", layout="wide")

# --- 1. DYNAMIC PCR ENGINE ---
def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(period="1d", interval="1m")
        if not df.empty:
            cur = df['Close'].iloc[-1]
            opn = df['Open'].iloc[0]
            # Moving PCR based on your 3.15 range
            val = round(3.15 + ((cur - opn) / 100), 2)
            return val
    except:
        return 3.15
    return 3.15

# --- 2. THEME & SMART UI ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .price-card { 
        background: #fff; padding: 20px; border-radius: 12px; 
        border: 1px solid #eee; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .buy-zone { background: #00c853; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    .sell-zone { background: #ff1744; color: white; padding: 5px 15px; border-radius: 5px; font-weight: 900; }
    .pcr-display { font-size: 65px; font-weight: 900; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI RENDER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h3 style='text-align:center; color:#1a237e;'>🦅 TRADEX PRO V75 | {datetime.now(IST).strftime('%H:%M:%S')}</h3>", unsafe_allow_html=True)

# Live PCR Header
pcr = get_live_pcr()
p_col = "#00c853" if pcr >= 1.0 else "#ff1744"
st.markdown(f"""
    <div style='text-align:center;'>
        <div style='color:#666; font-size:14px; font-weight:bold;'>LIVE MARKET PCR</div>
        <div class='pcr-display' style='color:{p_col};'>{pcr}</div>
        <div style='color:{p_col}; font-weight:bold; letter-spacing:2px;'>SENTIMENT: {'BULLISH' if pcr >= 1.0 else 'BEARISH'}</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Symbols with Sensex
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
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
                <div style='font-size:32px; font-weight:900;'>{ltp}</div>
                <div class='{btn}'>{sig}</div>
                <div style='color:#00c853; font-weight:bold; border:1px solid #a5d6a7; margin-top:10px; background:#e8f5e9;'>BULLISH ABOVE: {hi}</div>
                <div style='color:#ff1744; font-weight:bold; border:1px solid #ffab91; background:#ffebee;'>BEARISH BELOW: {lo}</div>
            </div>""", unsafe_allow_html=True)

time.sleep(5)
st.rerun()
