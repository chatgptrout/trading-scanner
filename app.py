import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX PRO V22", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-text { font-size: 24px; font-weight: 900; color: #121212; }
    .alert-container { background: #f0f4f8; border-radius: 15px; padding: 15px; margin-top: 20px; border: 1px solid #d1d9e6; }
    .btst-card { background: white; border-radius: 8px; padding: 12px; margin-top: 8px; border-right: 8px solid #2e7d32; display: flex; justify-content: space-between; }
    .stbt-card { background: white; border-radius: 8px; padding: 12px; margin-top: 8px; border-right: 8px solid #c62828; display: flex; justify-content: space-between; }
    </style>
    """, unsafe_allow_html=True)

def fetch_data(ticker, is_mcx=False):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty: return None
        ltp = data['Close'].iloc[-1]
        if is_mcx:
            ltp = ltp * 84.55 * (1.25 if "NG=F" in ticker else 1)
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if is_mcx: ema = ema * 84.55
        return {"p": round(ltp, 2), "ema": round(ema, 2), "is_bull": ltp > ema}
    except: return None

IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. MARKET STATUS
assets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NAT. GAS": "NG=F"}
for name, sym in assets.items():
    res = fetch_data(sym, is_mcx=("F" in sym))
    if res:
        color = "#2e7d32" if res['is_bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['is_bull'] else "BEARISH BELOW"
        st.markdown(f"<div class='index-card' style='border-left-color: {color};'><div style='font-size:12px; font-weight:bold; color:#757575;'>{name}</div><div style='display:flex; justify-content:space-between; align-items:center;'><div class='price-text'>₹{res['p']}</div><div style='color:{color}; font-weight:900; font-size:11px;'>{label}: {res['ema']}</div></div></div>", unsafe_allow_html=True)

# 2. HYBRID ALERTS (BTST & STBT)
st.markdown("<div class='alert-container'><h3>💰 BTST / STBT ALERTS</h3>", unsafe_allow_html=True)
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

for s in stocks:
    val = fetch_data(s)
    if val:
        if val['is_bull']: # BTST Signal
            st.markdown(f"<div class='btst-card'><div><b>🚀 BTST: {s.split('.')[0]}</b><br><span style='font-size:10px; color:gray;'>Trend: Bullish</span></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#2e7d32; font-size:10px; font-weight:bold;'>BUY</span></div></div>", unsafe_allow_html=True)
        else: # STBT Signal
            st.markdown(f"<div class='stbt-card'><div><b>🔻 STBT: {s.split('.')[0]}</b><br><span style='font-size:10px; color:gray;'>Trend: Bearish</span></div><div style='text-align:right;'><b>₹{val['p']}</b><br><span style='color:#c62828; font-size:10px; font-weight:bold;'>SELL</span></div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
