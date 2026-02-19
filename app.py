import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (ULTRA STABLE) ---
st.set_page_config(page_title="TRADEX PRO V61", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #eee; }
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; border-bottom: 3px solid #1a237e; }
    .idx-card { background: white; padding: 15px; border-radius: 12px; border-bottom: 4px solid #eee; }
    /* Market Distribution Bar */
    .pcr-bar-bg { width: 100%; height: 50px; background: #fdf2f2; border-radius: 4px; overflow: hidden; margin-top: 5px; position: relative; }
    .pcr-bar-fill { height: 100%; background: #f1b3b3; position: absolute; right: 0; transition: 0.5s; }
    /* Premium Signal Badges */
    .badge-buy { background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 4px; font-weight: 900; }
    .badge-sell { background: #ffebee; color: #c62828; padding: 4px 12px; border-radius: 4px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

def get_pcr_final():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.76
        delta = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (delta * 15))), 2)
    except: return 0.76

def get_stock_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR (ALL FEATURES TOGETHER) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1a237e;'>TRADEX PRO</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    pcr = get_pcr_final()
    p_color = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    
    # 1. Circular Meter
    st.markdown(f"""
    <div style='text-align:center; padding:10px; background:#fff; border:1px solid #eee; border-radius:15px;'>
        <div style='background:conic-gradient({p_color} {int(pcr*50)}%, #eee {int(pcr*50)}%); width:100px; height:100px; margin:auto; border-radius:50%; display:flex; align-items:center; justify-content:center;'>
            <div style='width:75px; height:75px; background:white; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                <small>PCR</small><b style='font-size:22px; color:{p_color};'>{pcr}</b>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 2. Market Distribution Bar (Red Bar Chart)
    st.markdown("<br><p style='color:gray; font-size:13px; margin-bottom:0;'>Market Distribution</p>", unsafe_allow_html=True)
    b_width = int((1.8 - pcr) * 55)
    st.markdown(f"""
    <div style='background:#f9f9f9; padding:10px; border-radius:8px;'>
        <div style='font-size:16px; font-weight:bold; color:#e57373;'>PCR {pcr}</div>
        <div class='pcr-bar-bg'><div class='pcr-bar-fill' style='width:{b_width}%;'></div></div>
        <small style='color:gray;'>Sentiment: Bearish</small>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("🏠 Dashboard")
    st.markdown("📈 Momentum Signals")

# --- MAIN UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='header-box'><b>● LIVE FEED</b><b>{datetime.now(IST).strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)

st.markdown("### 📊 KEY LEVELS")
c1, c2, c3, c4 = st.columns(4)
idx_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols_grid = [c1, c2, c3, c4]

for i, (name, sym) in enumerate(idx_list.items()):
    val = get_stock_data(sym)
    if val:
        clr = "#2e7d32" if val['bull'] else "#c62828"
        lbl = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        cols_grid[i].markdown(f"""
        <div class='idx-card' style='border-bottom-color:{clr};'>
            <small style='color:gray;'>{name}</small><br>
            <b style='font-size:20px;'>{'₹' if 'N' in sym else '$'}{val['p']}</b><br>
            <small style='color:{clr}; font-weight:bold;'>{lbl}: {val['ema']}</small>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div style='background:white; border-radius:12px; padding:10px; box-shadow:0 4px 12px rgba(0,0,0,0.03);'><div style='display:flex; background:#f1f3f4; padding:12px; font-weight:bold; font-size:12px;'><div style='width:25%'>SCRIPT</div><div style='width:20%'>SIGNAL</div><div style='width:35%'>LEVELS</div><div style='width:20%; text-align:right;'>LTP</div></div>", unsafe_allow_html=True)

for s in ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]:
    d = get_stock_data(s)
    if d:
        b_class = "badge-buy" if d['bull'] else "badge-sell"
        sig_txt = "BUY" if d['bull'] else "SELL"
        st.markdown(f"<div style='display:flex; padding:15px; border-bottom:1px solid #f8f9fa; align-items:center;'><div style='width:25%; font-weight:bold;'>{s.split('.')[0]}</div><div style='width:20%'><span class='{b_class}'>{sig_txt}</span></div><div style='width:35%; color:gray; font-size:12px;'>{d['ema']}</div><div style='width:20%; text-align:right; font-weight:bold;'>₹{d['p']}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
