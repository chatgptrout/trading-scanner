import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (WHITE THEME) ---
st.set_page_config(page_title="NIFTY BREAKOUT HUNTER", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 24px; font-weight: 900; color: #121212; }
    
    /* Alerts Styling */
    .btst-card { background: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 8px; border-right: 10px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
    .stbt-card { background: #ffebee; border-radius: 10px; padding: 15px; margin-top: 8px; border-right: 10px solid #c62828; display: flex; justify-content: space-between; align-items: center; }
    .breakout-tag { background: #1a237e; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        ltp = round(df['Close'].iloc[-1], 2)
        
        # MCX PRICE MATCH
        if ticker == "CL=F": ltp = round(ltp * 84.45, 2)
        elif ticker == "NG=F": ltp = round(ltp * 84.45 * 1.25, 2)
            
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        if ticker in ["CL=F", "NG=F"]: ema = round(ema * 84.45 * (1.25 if ticker=="NG=F" else 1), 2)
        
        # Breakout check: Current > EMA and Previous <= EMA
        is_break = ltp > ema and df['Close'].iloc[-2] <= (ema / (84.45 if ticker in ["CL=F", "NG=F"] else 1))
        
        return {"p": ltp, "ema": ema, "bull": ltp > ema, "break": is_break}
    except: return None

# --- 3. UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# SECTION 1: INDICES (Nifty, Bank Nifty, MCX)
market_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(market_list.items()):
    res = get_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        with cols[i % 2]:
            st.markdown(f"""
            <div class='index-card' style='border-left-color:{color};'>
                <div style='font-size:12px; font-weight:bold; color:#757575;'>{name}</div>
                <div class='price-text'>₹{res['p']}</div>
                <div style='color:{color}; font-size:10px; font-weight:bold;'>EMA: {res['ema']}</div>
            </div>""", unsafe_allow_html=True)

# SECTION 2: BTST / STBT BREAKOUT ALERTS
st.markdown("### 🎯 NIFTY 50 BREAKOUT ALERTS")
NIFTY_STOCKS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "BHARTIARTL.NS"]

found = False
for s in NIFTY_STOCKS:
    val = get_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']: # BTST
            found = True
            tag = "<span class='breakout-tag'>BREAKOUT</span>" if val['break'] else ""
            st.markdown(f"""
            <div class='btst-card'>
                <div><b>🚀 BTST: {t_name}</b> {tag}<br><small>Trend: Bullish</small></div>
                <div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-weight:bold;'>BUY</span></div>
            </div>""", unsafe_allow_html=True)
        else: # STBT
            found = True
            st.markdown(f"""
            <div class='stbt-card'>
                <div><b>🔻 STBT: {t_name}</b><br><small>Trend: Bearish</small></div>
                <div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#c62828; font-weight:bold;'>SELL</span></div>
            </div>""", unsafe_allow_html=True)

if not found:
    st.info("Scanning Nifty 50 stocks for breakouts...")

time.sleep(30)
st.rerun()
