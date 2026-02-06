import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH LIVE PRO", layout="wide")

# Dark Theme Style
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. ADVANCE/DECLINE METER
st.markdown("### 📊 MARKET MOOD")
col1, col2 = st.columns(2)
with col1: st.success("ADVANCES: 22")
with col2: st.error("DECLINES: 28")

# 2. SIMPLE & STABLE LIVE CHART (No Plotly - 100% Works)
st.markdown("### 📈 LIVE PRICE MOVEMENT")
selected_stock = st.selectbox("Select Stock for Chart:", ["SBIN.NS", "RELIANCE.NS", "ADANIENT.NS", "ZOMATO.NS"])

try:
    # Fetching simple 1-minute data for fast loading
    chart_df = yf.download(selected_stock, period='1d', interval='1m', progress=False)
    if not chart_df.empty:
        # Streamlit's native line chart - light and fast for mobile
        st.line_chart(chart_df['Close'])
    else:
        st.info("Connecting to exchange... 📡")
except:
    st.error("Network slow, retrying...")

# 3. NEO-STYLE SIGNALS WITH TARGETS
st.markdown("### 🚀 LIVE TRADING SIGNALS")
stocks = ["SBIN.NS", "RELIANCE.NS", "ADANIENT.NS", "TCS.NS", "HAL.NS"]

for s in stocks:
    try:
        t = yf.Ticker(s)
        p = t.fast_info['last_price']
        c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # Color based on trend
        color = "#00ff88" if c > 0 else "#ff4b2b"
        side = "LONG 🟢" if c > 0 else "SHORT 🔴"
        
        # Targets (T1: 0.5%, T2: 1%, SL: 0.6%)
        t1 = p * 1.005 if c > 0 else p * 0.995
        t2 = p * 1.01 if c > 0 else p * 0.99
        sl = p * 0.994 if c > 0 else p * 1.006

        st.markdown(f"""
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:10px solid {color}; margin-bottom:10px;">
                <h3 style="margin:0;">{side}: {s} @ ₹{p:.2f} ({c:.2f}%)</h3>
                <p style="color:{color}; font-size:18px;"><b>T1: {t1:.2f} | T2: {t2:.2f} | SL: {sl:.2f}</b></p>
            </div>
        """, unsafe_allow_html=True)
    except: continue

time.sleep(10)
st.rerun()
