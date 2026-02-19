import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V69", layout="wide")

# --- DYNAMIC CSS LOGIC ---
# Mock PCR value for demo - aapka live PCR yahan aayega
pcr_val = 0.76 
sentiment_color = "#ff1744" if pcr_val < 0.85 else "#00c853" # Red for Bearish, Green for Bullish

st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa; color: #1a1a1a; }}
    .pcr-card {{
        background: white; padding: 20px; border-radius: 15px;
        border: 2px solid {sentiment_color}; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .pcr-text {{ color: {sentiment_color}; font-size: 30px; font-weight: 900; }}
    .sentiment-tag {{ background: {sentiment_color}; color: white; padding: 5px 15px; border-radius: 5px; font-weight: bold; }}
    
    /* Neon Cards Style */
    .price-card {{ background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center; }}
    .buy-box {{ background: #00c853; color: white; padding: 8px; border-radius: 5px; font-weight: 900; }}
    .sell-box {{ background: #ff1744; color: white; padding: 8px; border-radius: 5px; font-weight: 900; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR PCR METER ---
with st.sidebar:
    st.markdown(f"""
        <div class='pcr-card'>
            <div style='color:#666; font-size:14px;'>PCR VALUE</div>
            <div class='pcr-text'>{pcr_val}</div>
            <br>
            <div class='sentiment-tag'>SENTIMENT: {'BEARISH' if pcr_val < 0.85 else 'BULLISH'}</div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
def get_data():
    symbols = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
    data = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="2d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high = round(df['High'].max(), 2)
            low = round(df['Low'].min(), 2)
            status = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
            data.append({"name": name, "ltp": ltp, "status": status, "bull": high, "bear": low})
    return data

st.markdown("<h2 style='text-align:center;'>🦅 TRADEX PRO V69 | SMART WHITE</h2>", unsafe_allow_html=True)

live_data = get_data()
cols = st.columns(4)
for i, item in enumerate(live_data):
    with cols[i]:
        box_class = "buy-box" if item['status'] == "BUY" else "sell-box"
        st.markdown(f"""
            <div class='price-card'>
                <div style='color:#777; font-size:12px;'>{item['name']}</div>
                <div style='font-size:32px; font-weight:900;'>{item['ltp']}</div>
                <div class='{box_class}'>{item['status']}</div>
                <div style='color:#00c853; font-weight:bold; margin-top:10px;'>BULLISH ABOVE: {item['bull']}</div>
                <div style='color:#ff1744; font-weight:bold;'>BEARISH BELOW: {item['bear']}</div>
            </div>
        """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
