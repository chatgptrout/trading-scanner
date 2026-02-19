import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG ---
st.set_page_config(page_title="TRADEX PRO V24", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 24px; font-weight: 900; color: #121212; }
    
    /* Hybrid Alert Styles */
    .btst-card { background: #e8f5e9; border-radius: 8px; padding: 12px; margin-top: 8px; border-right: 8px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
    .stbt-card { background: #ffebee; border-radius: 8px; padding: 12px; margin-top: 8px; border-right: 8px solid #c62828; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED MCX ENGINE ---
def get_mcx_matched_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty: return None
        
        raw_price = data['Close'].iloc[-1]
        raw_ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        # MCX MATCHING FORMULA (Current USD-INR + Multiplier)
        if ticker == "CL=F": # CRUDE OIL
            # 1 Barrel = 100 Units in MCX Approx
            mcx_price = raw_price * 84.45 
        elif ticker == "NG=F": # NATURAL GAS
            # NG Indian price is usually (Intl Price * 1.2 to 1.3) * USD-INR
            mcx_price = raw_price * 84.45 * 1.24
        else:
            mcx_price = raw_price
            
        mcx_ema = raw_ema * (84.45 if ticker in ["CL=F", "NG=F"] else 1)
        if ticker == "NG=F": mcx_ema = mcx_ema * 1.24

        return {"p": round(mcx_price, 2), "ema": round(mcx_ema, 2), "bull": mcx_price > mcx_ema}
    except: return None

# --- 3. UI ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDICES & MCX MATCH
market_list = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "CRUDE OIL (MCX)": "CL=F",
    "NAT. GAS (MCX)": "NG=F"
}

for name, sym in market_list.items():
    res = get_mcx_matched_data(sym)
    if res:
        color = "#2e7d32" if res['bull'] else "#c62828"
        lbl = "BULLISH ABOVE" if res['bull'] else "BEARISH BELOW"
        st.markdown(f"""
        <div class='index-card' style='border-left-color:{color};'>
            <div style='font-size:12px; font-weight:bold; color:#757575;'>{name}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='price-text'>₹{res['p']}</div>
                <div style='color:{color}; font-weight:900; font-size:11px;'>{lbl}: {res['ema']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. HYBRID ALERTS (BTST/STBT)
st.markdown("### 💰 BTST / STBT ALERTS")
stocks = ["RELIANCE.NS", "TCS.NS", "SBIN.NS", "HDFCBANK.NS"]

for s in stocks:
    val = get_mcx_matched_data(s)
    if val:
        t_name = s.split('.')[0]
        if val['bull']: # BTST (Green Card)
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {t_name}</b><br><small>Trend: Bullish</small></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-weight:bold;'>BUY</span></div></div>", unsafe_allow_html=True)
        else: # STBT (Red Card)
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {t_name}</b><br><small>Trend: Bearish</small></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#c62828; font-weight:bold;'>SELL</span></div></div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
