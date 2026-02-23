import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY SCANNER PRO", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem; background-color: #000;}</style>""", unsafe_allow_html=True)

# --- 1. DATA CENTER ---
def get_stock_data(symbol):
    try:
        df = yf.Ticker(symbol).history(period="1d", interval="1m")
        return df.iloc[-1] if not df.empty else None
    except: return None

# --- 2. LIVE NIFTY PRICE & LEVELS ---
df_nifty = yf.Ticker("^NSEI").history(period="1d")
if not df_nifty.empty:
    ltp = yf.Ticker("^NSEI").history(period="1d", interval="1m")['Close'].iloc[-1]
    hi, lo = df_nifty['High'].iloc[-1], df_nifty['Low'].iloc[-1]
    pcr_val = 2.01 # Latest Sentiment
    pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

    # Header: PCR
    st.markdown(f"<div style='text-align: center; color: {pcr_color}; font-size: 20px; font-weight: bold;'>PCR: {pcr_val} | {'BEARISH ⚠️' if pcr_val > 1.5 else 'BULLISH ✅'}</div>", unsafe_allow_html=True)

    # Big Nifty Price
    st.markdown(f"""
        <div style='text-align: center; background: #111; padding: 20px; border-radius: 15px; border: 2px solid {pcr_color}; margin: 10px 0;'>
            <p style='color: gray; margin: 0;'>NIFTY 50 LIVE SPOT</p>
            <h1 style='color: white; font-size: 60px; margin: 0;'>{ltp:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Bullish/Bearish Levels
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div style='text-align: center; background: #002b11; padding: 10px; border-radius: 10px;'><p style='color: #00ff66; margin:0; font-size: 12px;'>BULLISH ABOVE</p><h2 style='color: white; margin:0;'>{hi:,.2f}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='text-align: center; background: #2b0000; padding: 10px; border-radius: 10px;'><p style='color: #ff1744; margin:0; font-size: 12px;'>BEARISH BELOW</p><h2 style='color: white; margin:0;'>{lo:,.2f}</h2></div>", unsafe_allow_html=True)

# --- 3. LIVE SCANNER (BREAKOUT/BREAKDOWN) ---
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: yellow; text-align: center;'>⚡ LIVE SCANNER (STOCKS)</h3>", unsafe_allow_html=True)

# Example Stocks for scanning
watch_list = ["RELIANCE.NS", "HDFCBANK.NS", "TATASTEEL.NS", "SBIN.NS"]
b1, b2 = st.columns(2)

with b1:
    st.markdown("<p style='color: #00ff66; font-weight: bold;'>🚀 BREAKOUT</p>", unsafe_allow_html=True)
    for s in watch_list:
        data = get_stock_data(s)
        if data is not None and data['Close'] > data['Open']: # Simple Logic
            st.markdown(f"<div style='color: white; font-size: 14px;'><b>{s.split('.')[0]}</b>: {data['Close']:,.2f} ↑</div>", unsafe_allow_html=True)

with b2:
    st.markdown("<p style='color: #ff1744; font-weight: bold;'>📉 BREAKDOWN</p>", unsafe_allow_html=True)
    for s in watch_list:
        data = get_stock_data(s)
        if data is not None and data['Close'] < data['Open']:
            st.markdown(f"<div style='color: white; font-size: 14px;'><b>{s.split('.')[0]}</b>: {data['Close']:,.2f} ↓</div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: gray; font-size: 10px; margin-top: 20px;'>Last Sync: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)
time.sleep(10)
st.rerun()
