import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V25", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 22px; font-weight: 900; color: #121212; }
    .scanner-row { background: #fafafa; border-radius: 8px; padding: 10px; margin-bottom: 6px; border-left: 5px solid #1a237e; display: flex; justify-content: space-between; }
    .btst-card { background: #e8f5e9; border-radius: 8px; padding: 12px; margin-top: 6px; border-right: 8px solid #2e7d32; display: flex; justify-content: space-between; }
    .stbt-card { background: #ffebee; border-radius: 8px; padding: 12px; margin-top: 6px; border-right: 8px solid #c62828; display: flex; justify-content: space-between; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE ---
def get_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty: return None
        ltp = data['Close'].iloc[-1]
        
        # MCX PRICE MATCH LOGIC
        if ticker == "CL=F": ltp = ltp * 84.50 
        elif ticker == "NG=F": ltp = ltp * 84.50 * 1.26
            
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if ticker in ["CL=F", "NG=F"]: ema = ema * 84.50 * (1.26 if ticker=="NG=F" else 1)
        return {"p": round(ltp, 2), "ema": round(ema, 2), "bull": ltp > ema}
    except: return None

# --- 3. UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# SECTION 1: INDICES (Nifty, Bank Nifty, MCX)
market_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
for name, sym in market_list.items():
    res = get_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        st.markdown(f"<div class='index-card' style='border-left-color:{color};'><b>{name}</b><div style='display:flex; justify-content:space-between;'><span class='price-text'>₹{res['p']}</span><span style='color:{color}; font-weight:bold; font-size:11px;'>LEVEL: {res['ema']}</span></div></div>", unsafe_allow_html=True)

# SECTION 2: STOCK LIST (Wapas aa gayi!)
st.markdown("### 📊 LIVE STOCK LIST")
stocks = ["RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "TCS.NS"]
for s in stocks:
    val = get_data(s)
    if val:
        s_color = "#2e7d32" if val['bull'] else "#c62828"
        st.markdown(f"<div class='scanner-row' style='border-left-color:{s_color};'><span><b>{s.split('.')[0]}</b></span><span>₹{val['p']}</span></div>", unsafe_allow_html=True)

# SECTION 3: BTST / STBT ALERTS
st.markdown("### 💰 MOMENTUM ALERTS")
for s in stocks:
    val = get_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']:
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-size:10px;'>BUY</span></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#c62828; font-size:10px;'>SELL</span></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
