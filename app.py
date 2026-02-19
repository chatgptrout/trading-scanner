import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V64", layout="wide")

# --- NEON TERMINAL STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .price-card { 
        background: linear-gradient(145deg, #111, #1a1a1a);
        padding: 20px; border-radius: 15px; 
        border: 1px solid #333; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .buy-btn { background: #00ff88; color: black; padding: 10px 25px; border-radius: 8px; font-weight: 900; font-size: 20px; box-shadow: 0 0 15px #00ff88; }
    .sell-btn { background: #ff3e3e; color: white; padding: 10px 25px; border-radius: 8px; font-weight: 900; font-size: 20px; box-shadow: 0 0 15px #ff3e3e; }
    .ltp-text { font-size: 40px; font-weight: 900; color: #ffffff; margin: 10px 0; font-family: 'Courier New'; }
    .label-text { color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

def get_live_signals():
    symbols = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"}
    data = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            ema = round(df['Close'].ewm(span=9).mean().iloc[-1], 2)
            sig = "BUY" if ltp > ema else "SELL"
            data.append({"name": name, "ltp": ltp, "sig": sig, "ema": ema})
    return data

# Header
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#00ff88;'>🦅 TRADEX PRO TERMINAL V64</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:gray;'>LIVE SYNC: {datetime.now(IST).strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

live_data = get_live_signals()

# Grid Layout
cols = st.columns(len(live_data))
for i, item in enumerate(live_data):
    with cols[i]:
        sig_class = "buy-btn" if item['sig'] == "BUY" else "sell-btn"
        st.markdown(f"""
            <div class='price-card'>
                <div class='label-text'>{item['name']}</div>
                <div class='ltp-text'>${item['ltp']}</div>
                <div class='{sig_class}'>{item['sig']}</div>
                <div style='margin-top:15px; font-size:12px; color:#555;'>EMA 9: {item['ema']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
# Purana Momentum Section
st.subheader("🚀 MOMENTUM SIGNALS (STOCK MARKET)")
st.markdown("")

time.sleep(5)
st.rerun()
