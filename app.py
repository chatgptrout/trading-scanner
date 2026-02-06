import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH LIVE", layout="wide")

# Simple list for guaranteed results
tickers = ["RELIANCE.NS", "SBIN.NS", "INFY.NS", "TATAMOTORS.NS", "ZOMATO.NS"]

st.markdown("<h2 style='text-align:center;'>🚀 LIVE MOMENTUM TRACKER</h2>", unsafe_allow_html=True)

for sym in tickers:
    try:
        df = yf.download(sym, period='1d', interval='5m', progress=False)
        if not df.empty:
            price = df['Close'].iloc[-1]
            change = ((price - df['Open'].iloc[0]) / df['Open'].iloc[0]) * 100
            color = "#00ff88" if change > 0 else "#ff4b2b"
            
            st.markdown(f"""
                <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:8px solid {color}; margin-bottom:10px;">
                    <h3 style="margin:0;">{sym}: ₹{price:.2f}</h3>
                    <p style="color:{color}; font-size:18px;">Change: {change:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()
