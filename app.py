import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH LIVE", layout="wide")

# Sirf 5 bade stocks taaki jaldi load ho
tickers = ["RELIANCE.NS", "SBIN.NS", "HDFCBANK.NS", "TATAMOTORS.NS", "ZOMATO.NS"]

st.markdown("<h2 style='text-align:center;'>🚀 LIVE MOMENTUM TRACKER</h2>", unsafe_allow_html=True)

# Container for results
for sym in tickers:
    try:
        # 1-day data with 15m interval for faster fetch
        df = yf.download(sym, period='1d', interval='15m', progress=False)
        if not df.empty:
            price = df['Close'].iloc[-1]
            prev_close = df['Open'].iloc[0]
            change = ((price - prev_close) / prev_close) * 100
            color = "#00ff88" if change > 0 else "#ff4b2b"
            
            st.markdown(f"""
                <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:8px solid {color}; margin-bottom:10px;">
                    <h3 style="margin:0; color:white;">{sym}: ₹{price:.2f}</h3>
                    <p style="color:{color}; font-size:20px; font-weight:bold;">{change:.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write(f"Waiting for {sym} data...")
    except Exception as e:
        continue

time.sleep(20)
st.rerun()
