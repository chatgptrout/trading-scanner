import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

st.set_page_config(page_title="SANTOSH PRO COMMANDER", layout="wide")

# Custom CSS for Pro Look
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { display: flex; justify-content: space-around; background: #0d1b2a; padding: 15px; border-radius: 15px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; font-weight: bold; color: #00f2ff; }
    .screener-box { background: #0d1b2a; padding: 15px; border-radius: 15px; border-left: 5px solid #00f2ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 1. Navigation Bar
st.markdown('<div class="nav-bar"><span>🏠 Home</span><span>📊 Live Chart</span><span>🤖 AI Signals</span><span style="color:#00ff88">🔍 Screener Active</span></div>', unsafe_allow_html=True)

# 2. Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    # (Pichla Chart wala code yahan rahega)
    st.subheader("📊 LIVE CANDLESTICK CHART")
    target = st.selectbox("Select Asset", ["RELIANCE.NS", "^NSEI", "CL=F"], label_visibility="collapsed")
    df = yf.download(target, period='1d', interval='5m', progress=False)
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", plot_bgcolor="#010b14", paper_bgcolor="#010b14", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔍 LIVE SCREENER (MOMENTUM)")
    # Screener List
    stocks = {'RELIANCE': 'RELIANCE.NS', 'TATA MOTORS': 'TATAMOTORS.NS', 'SBI': 'SBIN.NS', 'HDFC': 'HDFCBANK.NS', 'ADANI': 'ADANIENT.NS'}
    
    for name, sym in stocks.items():
        try:
            sd = yf.download(sym, period='1d', interval='5m', progress=False)
            if not sd.empty:
                price = sd['Close'].iloc[-1]
                change = ((price - sd['Open'].iloc[0]) / sd['Open'].iloc[0]) * 100
                color = "#00ff88" if change > 0 else "#ff4b2b"
                
                st.markdown(f'''
                    <div class="screener-box">
                        <div style="display:flex; justify-content:space-between">
                            <span style="font-weight:bold">{name}</span>
                            <span style="color:{color}">{change:+.2f}%</span>
                        </div>
                        <div style="font-size:20px">₹{price:.2f}</div>
                    </div>
                ''', unsafe_allow_html=True)
        except:
            st.write(f"Scanning {name}...")

time.sleep(30)
st.rerun()
