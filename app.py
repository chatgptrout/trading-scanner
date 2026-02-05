import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

# Page Configuration
st.set_page_config(page_title="SANTOSH PRO COMMANDER", layout="wide")

# Custom CSS for Dark Neon Theme (Reference: image_1fe79e.jpg)
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar {
        display: flex; justify-content: space-around;
        background: #0d1b2a; padding: 15px;
        border-radius: 15px; border-bottom: 2px solid #00f2ff;
        margin-bottom: 20px; font-weight: bold; color: #00f2ff;
    }
    .status-card {
        background: #0d1b2a; padding: 20px; border-radius: 20px;
        border: 1px solid #1e3a5f; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Navigation Bar (Reference: image_1feeca.png)
st.markdown('<div class="nav-bar"><span>🏠 Home</span><span>📊 Live Chart</span><span style="color:#00ff88">🤖 AI Signals</span><span>🔍 Screener</span></div>', unsafe_allow_html=True)

# 2. Sidebar for Selection
target_stock = st.sidebar.selectbox("Select Asset to Chart", ["RELIANCE.NS", "^NSEI", "^NSEBANK", "CL=F"])

# 3. Layout: Chart on Left, Signals on Right
col1, col2 = st.columns([2, 1])

with col1:
    try:
        # Fetching Data for Chart (Reference: image_1fefa2.png)
        df = yf.download(target_stock, period='1d', interval='5m', progress=False)
        if not df.empty:
            df['EMA'] = ta.ema(df['Close'], length=20)
            
            # Creating Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name='Price'
            )])
            
            # Adding EMA Line (The blue/green line in your image)
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], line=dict(color='#00f2ff', width=2), name='20 EMA'))
            
            fig.update_layout(
                title=f"LIVE CHART: {target_stock}",
                template="plotly_dark",
                plot_bgcolor="#010b14", paper_bgcolor="#010b14",
                xaxis_rangeslider_visible=False,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.write("Chart Loading...")

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.header("AI SIGNALS")
    # Quick signals for watchlist
    for name, sym in {'NIFTY': '^NSEI', 'RELIANCE': 'RELIANCE.NS', 'CRUDE': 'CL=F'}.items():
        sd = yf.download(sym, period='1d', interval='15m', progress=False)
        if not sd.empty:
            price = sd['Close'].iloc[-1]
            rsi = ta.rsi(sd['Close'], length=14).iloc[-1]
            color = "#00ff88" if rsi > 60 else "#ff4b2b" if rsi < 40 else "#ffffff"
            st.markdown(f"**{name}**: <span style='color:{color}'>₹{price:.1f} (RSI: {rsi:.1f})</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh
time.sleep(30)
st.rerun()
