 import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

st.set_page_config(page_title="SANTOSH VOL-POWER AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { display: flex; justify-content: space-around; background: #0d1b2a; padding: 15px; border-radius: 15px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; font-weight: bold; color: #00f2ff; }
    .vol-card { background: #0d1b2a; padding: 15px; border-radius: 15px; border-left: 5px solid #00f2ff; margin-bottom: 10px; }
    .blink { animation: blinker 1.5s linear infinite; color: #00ff88; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# 1. Navigation Bar
st.markdown('<div class="nav-bar"><span>🏠 Home</span><span>📊 Chart</span><span style="color:#00ff88">🔍 Volume Screener Active</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    target = st.selectbox("Select Asset", ["RELIANCE.NS", "TATAMOTORS.NS", "ADANIENT.NS", "CL=F"], label_visibility="collapsed")
    df = yf.download(target, period='1d', interval='5m', progress=False)
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", plot_bgcolor="#010b14", paper_bgcolor="#010b14", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚀 VOLUME BURST SCANNER")
    # Extended watchlist for screening
    stocks = {'RELIANCE': 'RELIANCE.NS', 'TATA MOTORS': 'TATAMOTORS.NS', 'SBI': 'SBIN.NS', 'ADANI': 'ADANIENT.NS', 'CRUDE': 'CL=F'}
    
    for name, sym in stocks.items():
        try:
            # Fetching data to calculate average volume
            sd = yf.download(sym, period='2d', interval='15m', progress=False)
            if not sd.empty:
                curr_vol = sd['Volume'].iloc[-1]
                avg_vol = sd['Volume'].mean()
                price = sd['Close'].iloc[-1]
                change = ((price - sd['Open'].iloc[0]) / sd['Open'].iloc[0]) * 100
                
                # Volume Burst Logic: If current volume is 2x the average
                vol_status = ""
                if curr_vol > (avg_vol * 2):
                    vol_status = '<span class="blink">🔥 VOL BURST</span>'
                
                st.markdown(f'''
                    <div class="vol-card">
                        <div style="display:flex; justify-content:space-between">
                            <span style="font-weight:bold">{name} {vol_status}</span>
                            <span style="color:{"#00ff88" if change > 0 else "#ff4b2b"}">{change:+.2f}%</span>
                        </div>
                        <div style="font-size:22px">₹{price:.2f}</div>
                    </div>
                ''', unsafe_allow_html=True)
        except:
            st.write("📡")

time.sleep(20)
st.rerun()
