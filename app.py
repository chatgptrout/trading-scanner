import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (SAAF-SUTHRA WHITE) ---
st.set_page_config(page_title="TRADEX PRO V30", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .alert-card { border-radius: 10px; padding: 12px; margin-top: 6px; display: flex; justify-content: space-between; align-items: center; border-right: 8px solid; }
    .btst { background: #e8f5e9; border-right-color: #2e7d32; }
    .stbt { background: #ffebee; border-right-color: #c62828; }
    .breakout-tag { background: #ff9800; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

def get_live_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = round(df['Close'].iloc[-1], 2)
        
        # MCX MATCHING (Dhan/Groww Prices)
        if ticker == "CL=F": ltp = round(ltp * 84.45, 2)
        elif ticker == "NG=F": ltp = round(ltp * 84.45 * 1.25, 2)
            
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        if ticker in ["CL=F", "NG=F"]: ema = round(ema * 84.45 * (1.25 if ticker=="NG=F" else 1), 2)
        
        # Power Breakout: Current crosses EMA from below in the current 15m candle
        is_breakout = ltp > ema and df['Close'].iloc[-2] <= (ema / (84.45 if ticker in ["CL=F", "NG=F"] else 1))
        return {"p": ltp, "ema": ema, "bull": ltp > ema, "break": is_breakout}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDICES & MCX
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(indices.items()):
    res = get_live_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        with cols[i % 2]:
            st.markdown(f"<div class='index-card' style='border-left-color:{c};'><div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div><div style='font-size:22px; font-weight:900;'>₹{res['p']}</div><div style='color:{c}; font-size:10px; font-weight:bold;'>EMA: {res['ema']}</div></div>", unsafe_allow_html=True)

# 2. FULL NIFTY 50 SCANNER
st.markdown("### 🎯 NIFTY 50 SIGNALS & BREAKOUTS")
# Expanded list to catch breakouts even in bad markets
nifty_heavy = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS", "SUNPHARMA.NS", "AXISBANK.NS", "TITAN.NS", "TATAMOTORS.NS"]

for s in nifty_heavy:
    val = get_live_data(s)
    if val:
        t_name = s.split('.')[0]
        tag = "<span class='breakout-tag'>🔥 BREAKOUT</span>" if val['break'] else ""
        if val['bull']:
            st.markdown(f"<div class='alert-card btst'><div><b>🚀 BTST: {t_name}</b> {tag}</div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#2e7d32; font-weight:bold;'>BUY</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-card stbt'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#c62828; font-weight:bold;'>SELL</small></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
