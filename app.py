import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (CLEAN WHITE) ---
st.set_page_config(page_title="TRADEX PRO FINAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 24px; font-weight: 900; color: #121212; }
    .btst-card { background: #e8f5e9; border-radius: 10px; padding: 12px; margin-top: 8px; border-right: 10px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
    .stbt-card { background: #ffebee; border-radius: 10px; padding: 12px; margin-top: 8px; border-right: 10px solid #c62828; display: flex; justify-content: space-between; align-items: center; }
    .breakout-tag { background: #1a237e; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

def get_full_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = df['Close'].iloc[-1]
        
        # MCX MATCHING
        if ticker == "CL=F": ltp = ltp * 84.45
        elif ticker == "NG=F": ltp = ltp * 84.45 * 1.25
            
        ema = df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if ticker in ["CL=F", "NG=F"]: ema = ema * 84.45 * (1.25 if ticker=="NG=F" else 1)
        
        # Breakout logic
        is_break = ltp > ema and df['Close'].iloc[-2] <= (ema / (84.45 if ticker in ["CL=F", "NG=F"] else 1))
        return {"p": round(ltp, 2), "ema": round(ema, 2), "bull": ltp > ema, "break": is_break}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDICES & MCX (Dhan Match)
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(indices.items()):
    res = get_full_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        with cols[i % 2]:
            st.markdown(f"<div class='index-card' style='border-left-color:{c};'><div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div><div class='price-text'>₹{res['p']}</div><div style='color:{c}; font-size:10px; font-weight:bold;'>EMA: {res['ema']}</div></div>", unsafe_allow_html=True)

# 2. BREAKOUT & BTST/STBT ALERTS
st.markdown("### 🎯 NIFTY 50 SIGNALS & BREAKOUTS")
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS"]

for s in stocks:
    val = get_full_data(s)
    if val:
        t_name = s.split('.')[0]
        tag = "<span class='breakout-tag'>BREAKOUT</span>" if val['break'] else ""
        if val['bull']:
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b> {tag}</div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#2e7d32;'>BUY</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#c62828;'>SELL</small></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
