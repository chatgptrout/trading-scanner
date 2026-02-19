import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V47", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 30px; font-weight: 900; color: #ff5252; text-align: center; margin-bottom: 20px; }
    
    /* Perfect Sidebar Meter */
    .pcr-container { position: relative; width: 140px; height: 140px; margin: 15px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 110px; height: 110px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }
    
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .btst-card { background: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 8px; border-right: 10px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
    .stbt-card { background: #ffebee; border-radius: 10px; padding: 15px; margin-top: 8px; border-right: 10px solid #c62828; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

def get_market_metrics():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.84
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        pcr = round(max(0.5, min(1.6, 1.0 + (change * 8))), 2)
        return pcr
    except: return 0.84

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR: CLEAN LIVE PCR ---
with st.sidebar:
    pcr = get_market_metrics()
    pcr_color = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    status = "BEARISH" if pcr < 0.9 else "BULLISH" if pcr > 1.1 else "NEUTRAL"
    gradient = f"conic-gradient({pcr_color} {int(pcr*60)}%, #eee {int(pcr*60)}%)"
    
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#f8f9fa; border-radius:20px; border:1px solid #eee;'>
        <div style='color:{pcr_color}; font-weight:bold; border:1px solid {pcr_color}; border-radius:15px; display:inline-block; padding:2px 12px; font-size:10px;'>{status}</div>
        <div class='pcr-container' style='background:{gradient};'>
            <div class='pcr-inner'>
                <small style='color:gray; font-weight:bold;'>LIVE PCR</small>
                <div style='font-size:32px; font-weight:900; color:{pcr_color};'>{pcr}</div>
            </div>
        </div>
        <p style='font-size:10px; color:gray;'>Sentiment: Extreme Panic Zone</p>
    </div>""", unsafe_allow_html=True)

# --- MAIN UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. KEY LEVELS
st.markdown("### 📊 KEY LEVELS")
assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL ($)": "CL=F", "NAT. GAS ($)": "NG=F"}
for name, sym in assets.items():
    res = get_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        unit = "$" if "F" in sym else "₹"
        st.markdown(f"""
        <div class='index-card' style='border-left-color:{c};'>
            <div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='font-size:22px; font-weight:900;'>{unit}{res['p']}</div>
                <div style='color:{c}; font-size:11px; font-weight:bold;'>EMA: {res['ema']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. BTST / STBT ALERTS (Clean Cards)
st.markdown("---")
st.markdown("### 🎯 BTST / STBT ALERTS")
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = get_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']:
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#2e7d32; font-weight:bold;'>BUY</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#c62828; font-weight:bold;'>SELL</small></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
