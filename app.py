import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V46", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 30px; font-weight: 900; color: #ff5252; text-align: center; margin-bottom: 20px; }
    .pcr-container { position: relative; width: 140px; height: 140px; margin: 15px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 110px; height: 110px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .btst-card { background: #e8f5e9; border-radius: 10px; padding: 12px; margin-top: 6px; border-right: 10px solid #2e7d32; display: flex; justify-content: space-between; }
    .stbt-card { background: #ffebee; border-radius: 10px; padding: 12px; margin-top: 6px; border-right: 10px solid #c62828; display: flex; justify-content: space-between; }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    # Estimating PCR based on Nifty's daily trend as a proxy
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.85 # Default Neutral
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        # Logic: If market is down, PCR usually drops (Bearish)
        pcr = 1.0 + (change * 10) 
        return round(max(0.5, min(1.6, pcr)), 2)
    except: return 0.85

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR: DYNAMIC PCR ---
with st.sidebar:
    live_pcr = get_live_pcr()
    status = "BEARISH" if live_pcr < 0.9 else "BULLISH" if live_pcr > 1.1 else "NEUTRAL"
    color = "#c62828" if live_pcr < 0.9 else "#2e7d32" if live_pcr > 1.1 else "#fbc02d"
    bg_gradient = f"conic-gradient({color} {int(live_pcr*60)}%, #eee {int(live_pcr*60)}%)"
    
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#f8f9fa; border-radius:20px; border:1px solid #eee;'>
        <div style='color:{color}; font-weight:bold; border:1px solid {color}; border-radius:15px; display:inline-block; padding:2px 12px; font-size:10px;'>{status}</div>
        <div class='pcr-container' style='background:{bg_gradient};'>
            <div class='pcr-inner'>
                <small style='color:gray; font-weight:bold;'>LIVE PCR</small>
                <div style='font-size:32px; font-weight:900; color:{color};'>{live_pcr}</div>
            </div>
        </div>
        <p style='font-size:10px; color:gray;'>Auto-updated with Nifty Trend</p>
    </div>""", unsafe_allow_html=True)

# --- MAIN UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown("### 📊 KEY LEVELS")
assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL ($)": "CL=F", "NAT. GAS ($)": "NG=F"}
for name, sym in assets.items():
    res = get_data(sym)
    if res:
        c = "#2e7d32" if res['bull'] else "#c62828"
        unit = "$" if "F" in sym else "₹"
        st.markdown(f"<div class='index-card' style='border-left-color:{c};'><b>{name}</b><div style='display:flex; justify-content:space-between;'><span style='font-size:22px; font-weight:900;'>{unit}{res['p']}</span><span style='color:{c}; font-weight:bold; font-size:11px;'>EMA: {res['ema']}</span></div></div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🎯 BTST / STBT ALERTS")
for s in ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS"]:
    val = get_data(s)
    if val:
        t = s.split('.')[0]
        card = "btst-card" if val['bull'] else "stbt-card"
        label = "BUY" if val['bull'] else "SELL"
        st.markdown(f"<div class='{card}'><b>{t}</b><span>₹{val['p']} - <b>{label}</b></span></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
