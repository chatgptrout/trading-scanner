import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH FAST LIVE", layout="wide")

# Sirf 3 main stocks taaki load fast ho
tickers = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS"]

st.markdown("<h2 style='text-align:center;'>⚡ INSTANT MARKET TICKER</h2>", unsafe_allow_html=True)

# Direct data fetching with minimal delay
for sym in tickers:
    try:
        # Fetching only the last 1 day data with 1 minute interval for speed
        ticker_data = yf.Ticker(sym)
        price = ticker_data.fast_info['last_price']
        prev_close = ticker_data.fast_info['previous_close']
        change = ((price - prev_close) / prev_close) * 100
        
        color = "#00ff88" if change > 0 else "#ff4b2b"
        
        st.markdown(f"""
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:10px solid {color}; margin-bottom:10px;">
                <h3 style="margin:0; color:white;">{sym}</h3>
                <p style="font-size:24px; color:white; margin:5px 0;">₹{price:.2f}</p>
                <p style="color:{color}; font-size:20px; font-weight:bold;">{change:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.write(f"🔄 Refreshing {sym}...")

time.sleep(10)
st.rerun()
