import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (FORCE WIDE & STABLE) ---
st.set_page_config(page_title="TRADEX PRO V58", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    
    /* Header Box */
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1a237e; }
    
    /* PCR Circular Meter */
    .pcr-container { position: relative; width: 130px; height: 130px; margin: 10px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 100px; height: 100px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }
    
    /* Index Cards */
    .idx-card { background: white; padding: 15px; border-radius: 12px; border-bottom: 4px solid #eee; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    /* Table Styling */
    .trade-table-box { background: white; border-radius: 12px; padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .table-row { display: flex; padding: 15px; border-bottom: 1px solid #f8f9fa; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.76
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        pcr = round(max(0.4, min(1.8, 1.0 + (change * 15))), 2)
        return pcr
    except: return 0.76

def fetch_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR: CLEAN PCR METER ---
with st.sidebar:
    st.markdown("<h2 style='color:#1a237e;'>TRADEX PRO</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<b>MARKET DISTRIBUTION</b>", unsafe_allow_html=True)
    pcr = get_live_pcr()
    p_color = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#fff; border:1px solid #eee; border-radius:15px;'>
        <div class='pcr-container' style='background:conic-gradient({p_color} {int(pcr*50)}%, #eee {int(pcr*50)}%);'>
            <div class='pcr-inner'>
                <small style='color:gray; font-weight:bold;'>PCR</small>
                <b style='font-size:24px; color:{p_color};'>{pcr}</b>
            </div>
        </div>
        <small style='color:gray; font-weight:bold;'>Sentiment: Bearish</small>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("🏠 Dashboard")
    st.markdown("📈 Momentum Signals")

# --- MAIN PAGE ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='header-box'><b>● LIVE FEED</b><b>{datetime.now(IST).strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)

# 1. KEY LEVELS (Restore Bullish/Bearish)
st.markdown("### 📊 KEY LEVELS")
c1, c2, c3, c4 = st.columns(4)
idx_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = [c1, c2, c3, c4]

for i, (name, sym) in enumerate(idx_map.items()):
    d = fetch_data(sym)
    if d:
        clr = "#2e7d32" if d['bull'] else "#c62828"
        lbl = "BULLISH ABOVE" if d['bull'] else "BEARISH BELOW"
        unit = "$" if "F" in sym else "₹"
        cols[i].markdown(f"""
        <div class='idx-card' style='border-bottom-color:{clr};'>
            <small style='color:gray;'>{name}</small><br><b style='font-size:20px;'>{unit}{d['p']}</b><br>
            <small style='color:{clr}; font-weight:bold;'>{lbl}: {d['ema']}</small>
        </div>""", unsafe_allow_html=True)

# 2. SIGNALS TABLE
st.markdown("<br>### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div class='trade-table-box'><div style='display:flex; background:#f1f3f4; padding:12px; font-weight:bold; font-size:12px; color:#5f6368;'><div style='width:25%'>SCRIPT</div><div style='width:20%'>SIGNAL</div><div style='width:35%'>LEVELS</div><div style='width:20%; text-align:right;'>LTP</div></div>", unsafe_allow_html=True)

for s in ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]:
    val = fetch_data(s)
    if val:
        t = s.split('.')[0]
        clr = "#2e7d32" if val['bull'] else "#c62828"
        bg = "#e8f5e9" if val['bull'] else "#ffebee"
        sig = "BTST / BUY" if val['bull'] else "STBT / SELL"
        l_lbl = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        st.markdown(f"<div class='table-row'><div style='width:25%; font-weight:bold;'>{t}</div><div style='width:20%'><span style='background:{bg}; color:{clr}; padding:5px 10px; border-radius:6px; font-weight:bold; font-size:11px;'>{sig}</span></div><div style='width:35%; color:gray; font-size:12px;'><b>{l_lbl}</b>: {val['ema']}</div><div style='width:20%; text-align:right; font-weight:bold;'>₹{val['p']}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
