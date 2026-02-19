import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (STABLE & WIDE) ---
st.set_page_config(page_title="TRADEX PRO V61", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #eee; }
    
    /* Header */
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; border-bottom: 3px solid #1a237e; }
    
    /* Market Distribution (Red Bar) */
    .pcr-bar-bg { width: 100%; height: 50px; background: #fdf2f2; border-radius: 4px; overflow: hidden; margin-top: 5px; position: relative; }
    .pcr-bar-fill { height: 100%; background: #f1b3b3; position: absolute; right: 0; transition: 0.5s; }
    
    /* Index Cards */
    .idx-card { background: white; padding: 15px; border-radius: 12px; border-bottom: 4px solid #eee; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    /* Signal Badges */
    .badge-buy { background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    .badge-sell { background: #ffebee; color: #c62828; padding: 4px 12px; border-radius: 4px; font-weight: bold; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.76
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (change * 15))), 2)
    except: return 0.76

def fetch_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR: ALL DISTRIBUTION TOOLS ---
with st.sidebar:
    st.markdown("<h2 style='color:#1a237e;'>TRADEX PRO</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    pcr = get_live_pcr()
    p_color = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    
    # 1. Circular Meter (Nothing Deleted)
    st.markdown(f"""
    <div style='text-align:center; padding:10px; background:#fff; border:1px solid #eee; border-radius:15px; margin-bottom:15px;'>
        <div style='background:conic-gradient({p_color} {int(pcr*50)}%, #eee {int(pcr*50)}%); width:100px; height:100px; margin:auto; border-radius:50%; display:flex; align-items:center; justify-content:center;'>
            <div style='width:75px; height:75px; background:white; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                <small>PCR</small><b style='font-size:22px; color:{p_color};'>{pcr}</b>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 2. Red Bar Distribution (Nothing Deleted)
    st.markdown("<p style='color:gray; font-size:13px; margin-bottom:0;'>Market Distribution</p>", unsafe_allow_html=True)
    b_width = int((1.8 - pcr) * 55)
    st.markdown(f"""
    <div style='background:#f9f9f9; padding:10px; border-radius:8px;'>
        <div style='font-size:16px; font-weight:bold; color:#e57373;'>PCR {pcr}</div>
        <div class='pcr-bar-bg'><div class='pcr-bar-fill' style='width:{b_width}%;'></div></div>
        <small style='color:gray;'>Sentiment: Bearish</small>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("🏠 Dashboard")

# --- MAIN CONTENT ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='header-box'><b>● LIVE FEED</b><b>{datetime.now(IST).strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)

# 1. KEY LEVELS (Nifty/Crude Bullish/Bearish Protected)
st.markdown("### 📊 KEY LEVELS")
cols = st.columns(4)
idx_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols_grid = [cols[0], cols[1], cols[2], cols[3]]

for i, (name, sym) in enumerate(idx_map.items()):
    d = fetch_pro_data(sym)
    if d:
        clr = "#2e7d32" if d['bull'] else "#c62828"
        lbl = "BULLISH ABOVE" if d['bull'] else "BEARISH BELOW"
        cols_grid[i].markdown(f"""
        <div class='idx-card' style='border-bottom-color:{clr};'>
            <small style='color:gray; font-weight:bold;'>{name}</small><br>
            <b style='font-size:20px;'>{d['p']}</b><br>
            <small style='color:{clr}; font-weight:bold;'>{lbl}: {d['ema']}</small>
        </div>""", unsafe_allow_html=True)

# 2. MOMENTUM SIGNALS TABLE
st.markdown("<br>### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div style='background:white; border-radius:12px; padding:10px; box-shadow:0 4px 12px rgba(0,0,0,0.03);'><div style='display:flex; background:#f1f3f4; padding:12px; font-weight:bold; font-size:12px; color:#5f6368;'><div style='width:25%'>SCRIPT</div><div style='width:20%'>SIGNAL</div><div style='width:35%'>LEVELS</div><div style='width:20%; text-align:right;'>LTP</div></div>", unsafe_allow_html=True)

stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = fetch_pro_data(s)
    if val:
        t = s.split('.')[0]
        clr = "#2e7d32" if val['bull'] else "#c62828"
        bg = "badge-buy" if val['bull'] else "badge-sell"
        sig = "BUY" if val['bull'] else "SELL"
        l_lbl = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        st.markdown(f"<div style='display:flex; padding:15px; border-bottom:1px solid #f8f9fa; align-items:center;'><div style='width:25%; font-weight:bold;'>{t}</div><div style='width:20%'><span class='{bg}'>{sig}</span></div><div style='width:35%; color:gray; font-size:12px;'><b>{l_lbl}</b>: {val['ema']}</div><div style='width:20%; text-align:right; font-weight:bold;'>₹{val['p']}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
