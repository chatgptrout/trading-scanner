import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (ULTRA STABLE) ---
st.set_page_config(page_title="TRADEX PRO V59", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    
    /* Header Feed Bar */
    .feed-bar { background: white; padding: 12px 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid #1a237e; }
    
    /* PCR Meter Sidebar */
    .pcr-card { text-align: center; padding: 20px; background: #fff; border: 1px solid #eee; border-radius: 15px; margin-bottom: 20px; }
    .pcr-gauge { position: relative; width: 140px; height: 140px; margin: 10px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-val { width: 110px; height: 110px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 10px rgba(0,0,0,0.1); }

    /* Index Level Cards */
    .idx-card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); border-bottom: 5px solid #eee; transition: 0.3s; }
    .idx-price { font-size: 24px; font-weight: 900; color: #1a237e; margin: 8px 0; }

    /* Signal Table */
    .table-box { background: white; border-radius: 15px; padding: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.04); }
    .table-head { display: flex; background: #f8f9fa; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 13px; color: #5f6368; margin-bottom: 10px; border-bottom: 1px solid #eee; }
    .table-row { display: flex; padding: 18px; border-bottom: 1px solid #f8f9fa; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

def get_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.76
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        return round(max(0.4, min(1.8, 1.0 + (change * 15))), 2)
    except: return 0.76

def get_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR: BIG PCR METER ---
with st.sidebar:
    st.markdown("<h1 style='color:#1a237e; font-size:22px;'>TRADEX PRO</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<b>MARKET DISTRIBUTION</b>", unsafe_allow_html=True)
    pcr_val = get_pcr()
    p_clr = "#c62828" if pcr_val < 0.9 else "#2e7d32" if pcr_val > 1.1 else "#fbc02d"
    
    st.markdown(f"""
    <div class='pcr-card'>
        <div class='pcr-gauge' style='background:conic-gradient({p_clr} {int(pcr_val*50)}%, #eee {int(pcr_val*50)}%);'>
            <div class='pcr-val'>
                <small style='color:gray; font-weight:bold;'>PCR</small>
                <b style='font-size:30px; color:{p_clr};'>{pcr_val}</b>
            </div>
        </div>
        <div style='color:{p_clr}; font-weight:bold; font-size:14px; margin-top:10px;'>Sentiment: {'Bearish' if pcr_val < 0.9 else 'Bullish'}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("🏠 **Dashboard**")
    st.markdown("📈 **Momentum Signals**")

# --- MAIN PAGE ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"""
<div class='feed-bar'>
    <div style='font-weight:bold; color:#1a237e;'>● LIVE FEED</div>
    <div style='font-weight:900; color:#5f6368; font-size:18px;'>{datetime.now(IST).strftime('%H:%M:%S')}</div>
</div>
""", unsafe_allow_html=True)

# 1. KEY LEVELS (COLOR FIXED)
st.markdown("### 📊 KEY LEVELS")
c1, c2, c3, c4 = st.columns(4)
assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
cols = [c1, c2, c3, c4]

for i, (name, sym) in enumerate(assets.items()):
    res = get_pro_data(sym)
    if res:
        clr = "#2e7d32" if res['bull'] else "#c62828"
        lbl = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        unit = "$" if "F" in sym else "₹"
        cols[i].markdown(f"""
        <div class='idx-card' style='border-bottom-color:{clr};'>
            <small style='color:gray; font-weight:bold;'>{name}</small><br>
            <div class='idx-price'>{unit}{res['p']}</div>
            <div style='color:{clr}; font-weight:bold; font-size:11px;'>{lbl}: {res['ema']}</div>
        </div>""", unsafe_allow_html=True)

# 2. MOMENTUM SIGNALS
st.markdown("<br>### 🎯 MOMENTUM SIGNALS", unsafe_allow_html=True)
st.markdown("<div class='table-box'>", unsafe_allow_html=True)
st.markdown("<div class='table-head'><div style='width:25%'>SCRIPT</div><div style='width:20%'>SIGNAL</div><div style='width:35%'>LEVELS</div><div style='width:20%; text-align:right;'>LTP</div></div>", unsafe_allow_html=True)

stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = get_pro_data(s)
    if val:
        t = s.split('.')[0]
        clr = "#2e7d32" if val['bull'] else "#c62828"
        bg = "#e8f5e9" if val['bull'] else "#ffebee"
        sig = "BTST / BUY" if val['bull'] else "STBT / SELL"
        l_lbl = "BULLISH ABOVE" if val['bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='table-row'>
            <div style='width:25%; font-weight:bold; color:#1a237e;'>{t}</div>
            <div style='width:20%'><span style='background:{bg}; color:{clr}; padding:6px 12px; border-radius:8px; font-weight:bold; font-size:11px;'>{sig}</span></div>
            <div style='width:35%; color:#5f6368; font-size:12px;'><b>{l_lbl}</b>: {val['ema']}</div>
            <div style='width:20%; text-align:right; font-weight:bold;'>₹{val['p']}</div>
        </div>""", unsafe_allow_
