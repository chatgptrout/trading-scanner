import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V45", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 22px; font-weight: 900; color: #121212; }
    
    /* Circular PCR Meter */
    .pcr-container { position: relative; width: 150px; height: 150px; margin: 20px auto; border-radius: 50%; background: conic-gradient(#c62828 0% 40%, #2e7d32 40% 100%); display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 120px; height: 120px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    
    .btst-card { background: #e8f5e9; border-radius: 10px; padding: 12px; margin-top: 8px; border-right: 10px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
    .stbt-card { background: #ffebee; border-radius: 10px; padding: 12px; margin-top: 8px; border-right: 10px solid #c62828; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        ltp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        return {"p": ltp, "ema": ema, "bull": ltp > ema}
    except: return None

# --- SIDEBAR: PRO MARKET DISTRIBUTION ---
with st.sidebar:
    st.markdown("### 📊 Market Distribution")
    # Exact Circular Logic from your image
    st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#f8f9fa; border-radius:20px; border:1px solid #eee;'>
        <div style='color:#c62828; font-weight:bold; border:1px solid #c62828; border-radius:15px; display:inline-block; padding:2px 12px; font-size:11px;'>BEARISH</div>
        <div class='pcr-container'>
            <div class='pcr-inner'>
                <small style='color:gray; font-weight:bold;'>PCR</small>
                <div style='font-size:32px; font-weight:900; color:#c62828;'>0.59</div>
            </div>
        </div>
        <p style='font-size:11px; color:gray; font-weight:bold;'>Sentiment: Extreme Panic</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.success("Live Scanning: All Indices Active")

# --- MAIN UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. KEY LEVELS (Stability Fixed)
st.markdown("### 📉 KEY LEVELS (Bullish/Bearish)")
assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL ($)": "CL=F", "NAT. GAS ($)": "NG=F"}
for name, sym in assets.items():
    res = get_market_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        unit = "$" if "F" in sym else "₹"
        st.markdown(f"""
        <div class='index-card' style='border-left-color:{color};'>
            <div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='price-text'>{unit}{res['p']}</div>
                <div style='color:{color}; font-size:11px; font-weight:bold;'>{label}: {res['ema']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. MOMENTUM SIGNALS
st.markdown("### 🎯 MOMENTUM SIGNALS")
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]
for s in stocks:
    val = get_market_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']:
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#2e7d32; font-weight:bold;'>BUY</small></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b></div><div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#c62828; font-weight:bold;'>SELL</small></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
