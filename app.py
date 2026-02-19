import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V38", layout="centered")

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

def get_market_data(ticker):
    try:
        # 1m interval for high-speed tracking
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        
        ltp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        return {"p": ltp, "ema": ema, "bull": ltp > ema}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. KEY LEVELS (Nifty/BankNifty in ₹ | Crude/NG in $)
st.markdown("### 📊 KEY LEVELS (Bullish/Bearish)")
market_assets = {
    "NIFTY 50": "^NSEI", 
    "BANK NIFTY": "^NSEBANK", 
    "CRUDE OIL ($)": "CL=F", 
    "NAT. GAS ($)": "NG=F"
}

for name, sym in market_assets.items():
    res = get_market_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        unit = "$" if "F" in sym else "₹"
        st.markdown(f"""
        <div class='index-card' style='border-left-color:{color};'>
            <div style='font-size:12px; font-weight:bold; color:gray;'>{name}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='price-text'>{unit}{res['p']}</div>
                <div class='level-tag' style='color:{color}; background:{color}15;'>
                    {label}: {res['ema']}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. MOMENTUM SIGNALS (Nifty 50 Stocks)
st.markdown("### 🎯 MOMENTUM SIGNALS")
pro_stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]

for s in pro_stocks:
    val = get_market_data(s)
    if val:
        t_name = s.split('.')[0]
        style = "buy-zone" if val['bull'] else "sell-zone"
        side = "LONG" if val['bull'] else "SHORT"
        st.markdown(f"""
        <div class='action-card {style}'>
            <div><b>🚀 {t_name}</b></div>
            <div style='text-align:right;'><b>₹{val['p']}</b><br><small style='font-weight:bold;'>{side}</small></div>
        </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
