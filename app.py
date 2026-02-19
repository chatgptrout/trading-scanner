import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (CLEAN & SHARP) ---
st.set_page_config(page_title="BREAKOUT HUNTER V33", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 35px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .action-card { border-radius: 10px; padding: 18px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; border-right: 12px solid; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .buy-zone { background: #e8f5e9; border-right-color: #2e7d32; }
    .sell-zone { background: #ffebee; border-right-color: #c62828; }
    .breakout-flash { background: #ff9800; color: white; padding: 4px 10px; border-radius: 6px; font-size: 14px; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

def fetch_action_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = round(df['Close'].iloc[-1], 2)
        
        # MCX PRICE ADJUSTMENT
        if ticker == "CL=F": ltp = round(ltp * 84.45, 2)
        elif ticker == "NG=F": ltp = round(ltp * 84.45 * 1.25, 2)
            
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        if ticker in ["CL=F", "NG=F"]: ema = round(ema * 84.45 * (1.25 if ticker=="NG=F" else 1), 2)
        
        # Real-time Breakout Logic
        is_break = ltp > ema and df['Close'].iloc[-2] <= (ema / (84.45 if ticker in ["CL=F", "NG=F"] else 1))
        return {"p": ltp, "ema": ema, "bull": ltp > ema, "break": is_break}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🎯 ACTION ZONE: {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. MAJOR LEVELS (Nifty, Bank Nifty, MCX)
market_assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(market_assets.items()):
    res = fetch_action_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        with cols[i % 2]:
            st.markdown(f"<div class='index-card' style='border-left-color:{c};'><div style='font-size:12px; font-weight:bold; color:gray;'>{name}</div><div style='font-size:24px; font-weight:900;'>₹{res['p']}</div></div>", unsafe_allow_html=True)

# 2. PURE BREAKOUT & ENTRY ALERTS (Achaar nahi, sirf Paisa!)
st.markdown("---")
st.markdown("### 🔥 LIVE BREAKOUT & MOMENTUM ALERTS")
NIFTY_50_LIST = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "SUNPHARMA.NS"]

for s in NIFTY_50_LIST:
    val = fetch_action_data(s)
    if val:
        t_name = s.split('.')[0]
        # Breakout Tag will only show when EMA is crossed
        tag = "<span class='breakout-flash'>⚡ BREAKOUT</span>" if val['break'] else ""
        
        if val['bull']: # BTST Zone
            st.markdown(f"<div class='action-card buy-zone'><div><b>🚀 BTST: {t_name}</b> {tag}</div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-weight:bold;'>ENTER LONG</span></div></div>", unsafe_allow_html=True)
        else: # STBT Zone
            st.markdown(f"<div class='action-card sell-zone'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#c62828; font-weight:bold;'>ENTER SHORT</span></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
