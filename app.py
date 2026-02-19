import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V60", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1a237e; }
    .idx-card { background: white; padding: 15px; border-radius: 12px; border-bottom: 4px solid #eee; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .trade-table-box { background: white; border-radius: 12px; padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    /* Market Distribution Bar Style */
    .pcr-bar-bg { width: 100%; height: 60px; background: #fdf2f2; position: relative; border-radius: 4px; overflow: hidden; margin-top: 10px; }
    .pcr-bar-fill { height: 100%; background: #f1b3b3; position: absolute; right: 0; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.76
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (change * 15))), 2)
    except: return 0.76

def fetch_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1a237e;'>TRADEX PRO</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. Circular Meter
    pcr_val = get_live_pcr()
    p_color = "#c62828" if pcr_val < 0.9 else "#2e7d32" if pcr_val > 1.1 else "#fbc02d"
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#fff; border:1px solid #eee; border-radius:15px; margin-bottom:20px;'>
        <div style='background:conic-gradient({p_color} {int(pcr_val*50)}%, #eee {int(pcr_val*50)}%); width:100px; height:100px; margin:auto; border-radius:50%; display:flex; align-items:center; justify-content:center;'>
            <div style='width:75px; height:75px; background:white; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                <small>PCR</small><b style='font-size:22px; color:{p_color};'>{pcr_val}</b>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # 2. RESTORED Market Distribution Bar (YEH WAPAS AA GAYA)
    st.markdown("<p style='color:gray; font-size:14px; margin-bottom:0;'>Market Distribution</p>", unsafe_allow_html=True)
    bar_width = int((1.8 - pcr_val) * 60) # Logic for red bar width
    st.markdown(f"""
    <div style='background:#f9f9f9; padding:10px; border-radius:8px;'>
        <small style='color:gray;'>PCR</small>
        <div style='font-size:18px; font-weight:bold; color:#e57373;'>{pcr_val}</div>
        <div class='pcr-bar-bg'>
            <div class='pcr-bar-fill' style='width: {bar_width}%;'></div>
        </div>
        <small style='color:gray;'>Sentiment: Bearish</small>
    </div>""", unsafe_allow_html=True)

# --- MAIN PAGE (Levels & Table) ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='header-box'><b>● LIVE FEED</b><b>{datetime.now(IST).strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)

st.markdown("### 📊 KEY LEVELS")
c1, c2, c3, c4 = st.columns(4)
idx_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = [c1, c2, c3, c4]
for i, (name, sym) in enumerate(idx_map.items()):
    d = fetch_data(sym)
    if d:
        clr = "#2e7d32" if d['bull'] else "#c62828"
        cols[i].markdown(f"<div class='idx-card' style='border-bottom-color:{clr};'><small>{name}</small><br><b style='font-size:20px;'>{d['p']}</b><br><small style='color:{clr}; font-weight:bold;'>{('BULLISH ABOVE' if d['bull'] else 'BEARISH BELOW')}: {d['ema']}</small></div>", unsafe_allow_html=True)

st.markdown("<br>### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div class='trade-table-box'><div style='display:flex; background:#f1f3f4; padding:12px; font-weight:bold; font-size:12px;'><div style='width:25%'>SCRIPT</div><div style='width:20%'>SIGNAL</div><div style='width:35%'>LEVELS</div><div style='width:20%; text-align:right;'>LTP</div></div>", unsafe_allow_html=True)
for s in ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]:
    val = fetch_data(s)
    if val:
        clr = "#2e7d32" if val['bull'] else "#c62828"
        st.markdown(f"<div style='display:flex; padding:15px; border-bottom:1px solid #f8f9fa; align-items:center;'><div style='width:25%; font-weight:bold;'>{s.split('.')[0]}</div><div style='width:20%'><span style='background:#fdf2f2; color:{clr}; padding:5px 10px; border-radius:6px; font-weight:bold;'>{('BUY' if val['bull'] else 'SELL')}</span></div><div style='width:35%; color:gray; font-size:12px;'>{val['ema']}</div><div style='width:20%; text-align:right; font-weight:bold;'>{val['p']}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
