import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V43", layout="wide") # Layout wide kiya hai side-by-side ke liye

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .pcr-box { border: 1px solid #eee; border-radius: 15px; padding: 20px; text-align: center; background: #fafafa; }
    .pcr-value { font-size: 45px; font-weight: 900; color: #c62828; margin: 10px 0; }
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

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# --- TOP SECTION: LEVELS & PCR INDICATOR ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 KEY LEVELS")
    assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL ($)": "CL=F", "NAT. GAS ($)": "NG=F"}
    for name, sym in assets.items():
        res = get_market_data(sym)
        if res:
            color = "#2e7d32" if res['bull'] else "#c62828"
            unit = "$" if "F" in sym else "₹"
            st.markdown(f"""
            <div class='index-card' style='border-left-color:{color};'>
                <div style='font-size:11px; font-weight:bold; color:gray;'>{name}</div>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div style='font-size:22px; font-weight:900;'>{unit}{res['p']}</div>
                    <div style='color:{color}; font-size:10px; font-weight:bold;'>EMA: {res['ema']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("### 📉 MARKET SENTIMENT")
    # PCR Logic based on your image
    pcr_val = 0.59 
    st.markdown(f"""
    <div class='pcr-box'>
        <div style='color:#c62828; font-weight:bold; font-size:12px; border:1px solid #c62828; display:inline-block; padding:2px 8px; border-radius:20px;'>BEARISH</div>
        <div style='margin-top:15px; color:gray; font-size:12px; font-weight:bold;'>PCR</div>
        <div class='pcr-value'>{pcr_val}</div>
        <div style='width:100%; height:10px; background:linear-gradient(to right, #c62828 40%, #2e7d32 40%); border-radius:5px;'></div>
    </div>""", unsafe_allow_html=True)

# --- BOTTOM SECTION: MOMENTUM SIGNALS ---
st.markdown("---")
st.markdown("### 🎯 BTST / STBT ALERTS")
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]

for s in stocks:
    val = get_market_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']:
            st.markdown(f"""
            <div class='btst-card'>
                <div><b>🚀 BTST: {t_name}</b><br><small>Trend: Bullish</small></div>
                <div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#2e7d32; font-weight:bold;'>BUY</small></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='stbt-card'>
                <div><b>🔻 STBT: {t_name}</b><br><small>Trend: Bearish</small></div>
                <div style='text-align:right;'><b>₹{val['p']}</b><br><small style='color:#c62828; font-weight:bold;'>SELL</small></div>
            </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
