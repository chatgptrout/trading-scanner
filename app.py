import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V34", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 24px; font-weight: 900; color: #121212; }
    .level-tag { font-size: 11px; font-weight: 900; padding: 4px 8px; border-radius: 4px; }
    .action-card { border-radius: 10px; padding: 15px; margin-top: 8px; display: flex; justify-content: space-between; align-items: center; border-right: 10px solid; }
    .buy-zone { background: #e8f5e9; border-right-color: #2e7d32; }
    .sell-zone { background: #ffebee; border-right-color: #c62828; }
    </style>
    """, unsafe_allow_html=True)

def get_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = round(df['Close'].iloc[-1], 2)
        
        # MCX MATCHING
        if ticker == "CL=F": ltp = round(ltp * 84.45, 2)
        elif ticker == "NG=F": ltp = round(ltp * 84.45 * 1.25, 2)
            
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        if ticker in ["CL=F", "NG=F"]: ema = round(ema * 84.45 * (1.25 if ticker=="NG=F" else 1), 2)
        
        return {"p": ltp, "ema": ema, "bull": ltp > ema}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. LEVELS SECTION (WAPAS AA GAYA!)
st.markdown("### 📊 KEY LEVELS (Bullish/Bearish)")
market_assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}

for name, sym in market_assets.items():
    res = get_pro_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='index-card' style='border-left-color:{color};'>
            <div style='font-size:12px; font
