import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. SETTINGS ---
st.set_page_config(page_title="TRADEX PRO V20", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 35px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 26px; font-weight: 900; color: #121212; }
    .btst-item { background: #fffde7; border-radius: 10px; padding: 12px; margin-top: 8px; border-right: 8px solid #fbc02d; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (MATCHING LOGIC) ---
def fetch_matching_data(ticker, is_mcx=False):
    try:
        # 1m interval for latest LTP
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty: return None
        
        ltp = data['Close'].iloc[-1]
        
        # MCX Conversion for Crude/NG to match Indian Apps
        if is_mcx:
            if "CL=F" in ticker: ltp = ltp * 84.45 # USD-INR current
            elif "NG=F" in ticker: ltp = ltp * 84.45 * 1.22 # Units adjustment
            
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if is_mcx: ema = ema * 84.45

        return {"p": round(ltp, 2), "ema": round(ema, 2), "bull": ltp > ema}
    except: return None

# --- 3. UI RENDER ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDEX & COMMODITY
assets = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "CRUDE OIL (MCX)": "CL=F",
    "NATURAL GAS (MCX)": "NG=F"
}

for name, sym in assets.items():
    is_comm = True if "F" in sym else False
    res = fetch_matching_data(sym, is_mcx=is_comm)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='index-card' style='border-left-color: {color};'>
            <div style='font-size:12px; font-weight:bold; color:#757575;'>{name}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='price-text'>₹{res['p']}</div>
                <div style='color:{color}; font-weight:900; font-size:11px;'>{label}: {res['ema']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. BTST / SWING ALERTS (FIXED)
st.markdown("### 💰 BTST / SWING ALERTS")
btst_list = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS"]
found_btst = False

for b in btst_list:
    val = fetch_matching_data(b)
    # Agar Bullish hai toh hi dikhao, warna "Scanning..." dikhao
    if val and val['bull']:
        found_btst = True
        st.markdown(f"""
        <div class='btst-item'>
            <div><b>🚀 {b.split('.')[0]}</b><br><span style='font-size:10px; color:gray;'>High Momentum Pick</span></div>
            <div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-size:10px;'>STRONG</span></div>
        </div>""", unsafe_allow_html=True)

if not found_btst:
    st.info("Searching for Strong BTST setups... No stocks currently in Buy Zone.")

time.sleep(30)
st.rerun()
