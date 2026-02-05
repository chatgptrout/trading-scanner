import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

# Dashboard Configuration
st.set_page_config(page_title="SANTOSH AI COMMANDER", layout="wide")

# Futuristic Dark Theme CSS
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

# 1. Navigation Bar
st.markdown('<div class="nav-bar"><span>🏠 Home</span><span style="color:#00ff88">📊 Live Chart</span><span>🤖 AI Signals</span><span>🔍 Screener</span></div>', unsafe_allow_html=True)

# 2. Sidebar for Stock Selection
target_stock = st.sidebar.selectbox("Select Asset", ["RELIANCE.NS", "^NSEI", "^NSEBANK", "CL=F"])

col1, col2 = st.columns([2, 1])

with col1:
    try:
        # Fetching Data for Candlestick Chart
        df = yf.download(target_stock, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 20:
            df['EMA'] = ta.ema(df['Close'], length=20)
            
            # Candlestick Chart (Reference: image_1fefa2.png)
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name='Market Price'
            )])
            
            # Neon EMA Line
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], line=dict(color='#00f2ff', width=2), name='20 EMA'))
            
            fig.update_layout(
                template="plotly_dark", plot_bgcolor="#010b14", paper_bgcolor="#010b14",
                xaxis_rangeslider_visible=False, height=500, margin=dict(t=30, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart Update Pending: {e}")

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("🎯 AI MOMENTUM")
    
    watchlist = {'NIFTY': '^NSEI', 'RELIANCE': 'RELIANCE.NS', 'CRUDE': 'CL=F'}
    for name, sym in watchlist.items():
        try:
            sd = yf.download(sym, period='5d', interval='15m', progress=False)
            if not sd.empty and len(sd) > 14:
                # Safe RSI calculation to avoid image_204521 error
                rsi_series = ta.rsi(sd['Close'], length=14)
                current_rsi = rsi_series.iloc[-1]
                current_price = sd['Close'].iloc[-1]
                
                color = "#00ff88" if current_rsi > 62 else "#ff4b2b" if current_rsi < 35 else "#ffffff"
                signal = "BULLISH 🐂" if current_rsi > 62 else "BEARISH 🐻" if current_rsi < 35 else "NEUTRAL ⚖️"
                
                st.markdown(f"**{name}**: ₹{current_price:.1f}")
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>{signal} (RSI: {current_rsi:.1f})</span>", unsafe_allow_html=True)
                st.divider()
        except:
            st.write(f"Scanning {name}...")
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh every 30 seconds
time.sleep(30)
st.rerun()
