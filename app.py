import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (ORIGINAL WHITE THEME) ---
st.set_page_config(page_title="TRADEX PRO V31", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .scanner-box { background: #fafafa; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 12px solid #1a237e; display: flex; justify-content: space-between; align-items: center; }
    .btst-card { background: #e8f5e9; border-radius: 8px; padding: 12px; margin-top: 6px; border-right: 8px solid #2e7d32; display: flex; justify-content: space-between; }
    .stbt-card { background: #ffebee; border-radius: 8px; padding: 12px; margin-top: 6px; border-right: 8px solid #c62828; display: flex; justify-content: space-between; }
    .breakout-tag { background: #ff9800; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = df['Close'].iloc[-1]
        
        # MCX MATCHING
        if ticker == "CL=F": ltp = ltp * 84.45
        elif ticker == "NG=F": ltp = ltp * 84.45 * 1.25
            
        ema = df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if ticker in ["CL=F", "NG=F"]: ema = ema * 84.45 * (1.25 if ticker=="NG=F" else 1)
        
        is_break = ltp > ema and df['Close'].iloc[-2] <= (ema / (84.45 if ticker in ["CL=F", "NG=F"] else 1))
        return {"p": round(ltp, 2), "ema": round(ema, 2), "bull": ltp > ema, "break": is_break}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDICES & MCX
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(indices.items()):
    res = get_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        with cols[i % 2]:
            st.markdown(f"<div class='index-card' style='border-left-color:{c};'><div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div><div style='font-size:22px; font-weight:900;'>₹{res['p']}</div></div>", unsafe_allow_html=True)

# 2. LIVE STOCK SCANNER (ORIGINAL LIST)
st.markdown("### 📊 LIVE STOCK LIST")
stocks = ["RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "TCS.NS", "INFY.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = get_data(s)
    if val:
        color = "#2e7d32" if val['bull'] else "#c62828"
        st.markdown(f"<div class='scanner-box' style='border-left-color:{color};'><b>{s.split('.')[0]}</b><span>₹{val['p']}</span></div>", unsafe_allow_html=True)

# 3. BTST / STBT & BREAKOUT ALERTS
st.markdown("### 💰 MOMENTUM ALERTS")
for s in stocks:
    val = get_data(s)
    if val:
        t_name = s.split('.')[0]
        tag = "<span class='breakout-tag'>BREAKOUT</span>" if val['break'] else ""
        if val['bull']:
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b> {tag}</div><div style='text-align:right;'><b>₹{val['p']}</b><br><small>BUY</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small>SELL</small></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
