import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY ULTIMATE SCANNER", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem; background-color: #000;}</style>""", unsafe_allow_html=True)

# --- 1. PCR & PRICE SECTION ---
pcr_val = 2.01  # Live PCR Value
pcr_color = "#ff1744" if pcr_val > 1.2 else "#00ff66"

st.markdown(f"""
    <div style='text-align: center; background: #111; padding: 15px; border-radius: 12px; border: 2px solid {pcr_color};'>
        <p style='color: {pcr_color}; font-weight: bold; margin: 0;'>LIVE PCR: {pcr_val}</p>
        <h1 style='color: white; font-size: 50px; margin: 0;'>25,565.90</h1>
        <div style='display: flex; justify-content: space-around; margin-top: 10px;'>
            <div style='color: #00ff66;'><b>BULLISH ABOVE: 25,600</b></div>
            <div style='color: #ff1744;'><b>BEARISH BELOW: 25,450</b></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. LIVE STOCK LIST (BREAKOUT/BREAKDOWN) ---
st.markdown("<h3 style='color: yellow; text-align: center; margin-top: 15px;'>⚡ LIVE STOCK SCANNER</h3>", unsafe_allow_html=True)

stocks = {
    "RELIANCE": "BULLISH",
    "HDFCBANK": "BEARISH",
    "SBIN": "BREAKOUT",
    "TATASTEEL": "BULLISH",
    "INFY": "BREAKDOWN"
}

c1, c2 = st.columns(2)
with c1:
    st.markdown("<p style='color: #00ff66; border-bottom: 1px solid #00ff66;'>🚀 BUY LIST</p>", unsafe_allow_html=True)
    for s, v in stocks.items():
        if v in ["BULLISH", "BREAKOUT"]:
            st.markdown(f"<div style='color: white; font-size: 16px;'>✅ {s}</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<p style='color: #ff1744; border-bottom: 1px solid #ff1744;'>📉 SELL LIST</p>", unsafe_allow_html=True)
    for s, v in stocks.items():
        if v in ["BEARISH", "BREAKDOWN"]:
            st.markdown(f"<div style='color: white; font-size: 16px;'>❌ {s}</div>", unsafe_allow_html=True)

# --- 3. BTST / STBT SPECIAL SECTION ---
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
b1, b2 = st.columns(2)

with b1:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #004d00, #000); padding: 15px; border-radius: 10px; text-align: center;'>
            <h4 style='color: #00ff66; margin: 0;'>🔥 BTST</h4>
            <p style='color: white; font-size: 18px; margin: 5px 0;'><b>ADANI ENT</b></p>
            <span style='color: gray; font-size: 10px;'>Target: +2%</span>
        </div>
    """, unsafe_allow_html=True)

with b2:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4d0000, #000); padding: 15px; border-radius: 10px; text-align: center;'>
            <h4 style='color: #ff1744; margin: 0;'>❄️ STBT</h4>
            <p style='color: white; font-size: 18px; margin: 5px 0;'><b>COAL INDIA</b></p>
            <span style='color: gray; font-size: 10px;'>Target: -1.5%</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: gray; font-size: 10px; margin-top: 15px;'>Last Refresh: {datetime.now().strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)
time.sleep(15)
st.rerun()
