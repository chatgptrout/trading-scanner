import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (PREMIUM DASHBOARD LOOK) ---
st.set_page_config(page_title="TRADEX PRO V53", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    
    /* Header Branding */
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
    .logo-text { font-size: 26px; font-weight: 900; color: #1a237e; letter-spacing: -1px; }
    .live-dot { height: 10px; width: 10px; background-color: #ff5252; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }

    /* Professional Table Styling */
    .trade-container { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); }
    .table-header { display: flex; background: #f1f3f4; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 13px; color: #5f6368; margin-bottom: 10px; }
    .table-row { display: flex; padding: 15px; border-bottom: 1px solid #f1f3f4; align-items: center; transition: 0.3s; }
    .table-row:hover { background-color: #fcfcfc; }
    
    /* Sidebar PCR Meter */
    .pcr-sidebar-box { text-align: center; padding: 15px; background: #fff; border: 1px solid #eee; border-radius: 15px; margin-top: 20px; }
    .pcr-container { position: relative; width: 120px; height: 120px; margin: 10px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 95px; height: 95px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 5px rgba(0,0,0,0.1); }
    
    /* Badges */
    .badge-buy { background: #e8f5e9; color: #2e7d32; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-sell { background: #ffebee; color: #c62828; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (change * 12))), 2)
    except: return 0.85

def get_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR (Menu + PCR Meter) ---
with st.sidebar:
    st.markdown("<div class='logo-text'>TRADEX PRO</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:green; font-weight:bold; font-size:12px;'>● MARKET ONLINE</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("📊 **Dashboard**")
    st.markdown("🔥 **Momentum Signals**")
    st.markdown("---")
    
    # PCR Meter (Automatic Change)
    st.markdown("**Market Distribution**")
    pcr = get_live_pcr()
    c = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    st.markdown(f"""
    <div class='pcr-sidebar-box'>
        <div class='pcr-container' style='background:conic-gradient({c} {int(pcr*55)}%, #eee {int(pcr*55)}%);'>
            <div class='pcr-inner'><small>PCR</small><div style='font-size:26px; font-weight:900; color:{c};'>{pcr}</div></div>
        </div>
        <small style='color:gray;'>Sentiment: {'Bearish' if pcr < 0.9 else 'Bullish'}</small>
    </div>""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"""
<div class='header-box'>
    <div style='font-weight:bold; color:#1a237e;'><span class='live-dot'></span> LIVE MARKET FEED</div>
    <div style='font-weight:900; color:#5f6368;'>{datetime.now(IST).strftime('%H:%M:%S')}</div>
</div>
""", unsafe_allow_html=True)

# 1. KEY INDICES (Top Row)
cols = st.columns(4)
idx = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL ($)": "CL=F", "NAT. GAS ($)": "NG=F"}
for i, (name, sym) in enumerate(idx.items()):
    d = get_pro_data(sym)
    if d:
        with cols[i]:
            st.markdown(f"<div style='background:white; padding:15px; border-radius:12px; border-bottom:4px solid {'#2e7d32' if d['bull'] else '#c62828'};'><small style='color:gray;'>{name}</small><br><b style='font-size:20px;'>{d['p']}</b></div>", unsafe_allow_html=True)

# 2. THE SIGNAL TABLE (Everything from Purana Version)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='trade-container'>", unsafe_allow_html=True)
st.markdown("""
<div class='table-header'>
    <div style='width:25%'>SCRIPT</div>
    <div style='width:20%'>SIGNAL</div>
    <div style='width:35%'>LEVELS (Bullish Above/Bearish Below)</div>
    <div style='width:20%; text-align:right;'>LTP</div>
</div>
""", unsafe_allow_html=True)

stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = get_pro_data(s)
    if val:
        t_name = s.split('.')[0]
        badge = "badge-buy" if val['bull'] else "badge-sell"
        sig = "BTST / BUY" if val['bull'] else "STBT / SELL"
        lvl_label = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        
        st.markdown(f"""
        <div class='table-row'>
            <div style='width:25%; font-weight:bold; color:#1a237e;'>{t_name}</div>
            <div style='width:20%'><span class='{badge}'>{sig}</span></div>
            <div style='width:35%; color:#5f6368; font-size:13px;'><b>{lvl_label}</b>: {val['ema']}</div>
            <div style='width:20%; text-align:right; font-weight:bold;'>₹{val['p']}</div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10) # Fast Refresh
st.rerun()
