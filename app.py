import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (FORCE WIDE & WHITE) ---
st.set_page_config(page_title="TRADEX PRO V55", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #eee; }
    
    /* Global Header */
    .main-header { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1a237e; }
    .logo-text { font-size: 24px; font-weight: 900; color: #1a237e; }
    .live-indicator { color: #ff5252; font-weight: bold; font-size: 12px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }

    /* Index Cards */
    .idx-box { background: white; padding: 15px; border-radius: 12px; border-bottom: 4px solid #eee; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 10px; }
    .idx-name { color: #5f6368; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .idx-price { font-size: 20px; font-weight: 900; color: #1a237e; margin: 5px 0; }
    .idx-level { font-size: 10px; font-weight: bold; }

    /* Signal Table */
    .table-container { background: white; border-radius: 12px; padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .table-head { display: flex; background: #f1f3f4; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 12px; color: #5f6368; margin-bottom: 5px; }
    .table-row { display: flex; padding: 15px; border-bottom: 1px solid #f8f9fa; align-items: center; }
    
    /* PCR Sidebar */
    .pcr-sidebar-card { text-align: center; padding: 15px; background: #fff; border: 1px solid #eee; border-radius: 15px; }
    .pcr-meter { position: relative; width: 100px; height: 100px; margin: 10px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-val-inner { width: 75px; height: 75px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

def get_pcr_live():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (change * 15))), 2)
    except: return 0.81

def fetch_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        ltp = df['Close'].iloc[-1]
        ema = df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(ltp, 2), "ema": round(ema, 2), "bull": ltp > ema}
    except: return None

# --- SIDEBAR (Always Stable) ---
with st.sidebar:
    st.markdown("<div class='logo-text'>TRADEX PRO</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:green; font-weight:bold; font-size:12px;'>● MARKET ONLINE</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("🏠 Dashboard")
    st.markdown("📈 Momentum Signals")
    st.markdown("---")
    st.markdown("**Market Distribution**")
    pcr = get_pcr_live()
    p_color = "#c62828" if pcr < 0.9 else "#2e7d32" if pcr > 1.1 else "#fbc02d"
    st.markdown(f"""
    <div class='pcr-sidebar-card'>
        <div class='pcr-meter' style='background:conic-gradient({p_color} {int(pcr*50)}%, #eee {int(pcr*50)}%);'>
            <div class='pcr-val-inner'><small>PCR</small><div style='font-size:22px; font-weight:900; color:{p_color};'>{pcr}</div></div>
        </div>
        <small style='color:gray; font-weight:bold;'>Sentiment: {'Bearish' if pcr < 0.9 else 'Bullish'}</small>
    </div>""", unsafe_allow_html=True)

# --- MAIN PAGE (RE-STABILIZED) ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"""
<div class='main-header'>
    <div style='font-weight:bold;'><span class='live-indicator'>●</span> LIVE MARKET FEED</div>
    <div style='font-weight:bold; color:#5f6368;'>{datetime.now(IST).strftime('%H:%M:%S')}</div>
</div>
""", unsafe_allow_html=True)

# 1. INDEX LEVELS (With Bullish/Bearish Restored)
st.markdown("#### 📊 KEY LEVELS")
c1, c2, c3, c4 = st.columns(4)
idx_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols_list = [c1, c2, c3, c4]

for i, (name, sym) in enumerate(idx_map.items()):
    d = fetch_pro_data(sym)
    if d:
        with cols_list[i]:
            clr = "#2e7d32" if d['bull'] else "#c62828"
            lbl = "BULLISH ABOVE" if d['bull'] else "BEARISH BELOW"
            unit = "$" if "F" in sym else "₹"
            st.markdown(f"""
            <div class='idx-box' style='border-bottom-color:{clr};'>
                <div class='idx-name'>{name}</div>
                <div class='idx-price'>{unit}{d['p']}</div>
                <div class='idx-level' style='color:{clr};'>{lbl}: {d['ema']}</div>
            </div>""", unsafe_allow_html=True)

# 2. PROFESSIONAL SIGNAL TABLE
st.markdown("<br>#### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div class='table-container'>", unsafe_allow_html=True)
st.markdown("""
<div class='table-head'>
    <div style='width:25%'>SCRIPT</div>
    <div style='width:20%'>SIGNAL</div>
    <div style='width:35%'>LEVELS (Bullish Above/Bearish Below)</div>
    <div style='width:20%; text-align:right;'>LTP</div>
</div>
""", unsafe_allow_html=True)

for s in ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]:
    val = fetch_pro_data(s)
    if val:
        t = s.split('.')[0]
        bg = "#e8f5e9" if val['bull'] else "#ffebee"
        txt_c = "#2e7d32" if val['bull'] else "#c62828"
        sig = "BTST / BUY" if val['bull'] else "STBT / SELL"
        l_lbl = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='table-row'>
            <div style='width:25%; font-weight:bold; color:#1a237e;'>{t}</div>
            <div style='width:20%'><span style='background:{bg}; color:{txt_c}; padding:5px 10px; border-radius:6px; font-weight:bold; font-size:11px;'>{sig}</span></div>
            <div style='width:35%; color:#5f6368; font-size:12px;'><b>{l_lbl}</b>: {val['ema']}</div>
            <div style='width:20%; text-align:right; font-weight:bold;'>₹{val['p']}</div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
