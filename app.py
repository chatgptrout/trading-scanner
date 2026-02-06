import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH CLICK-SCANNER", layout="wide")

# Theme
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. SIDEBAR SELECTION (Click jaisa kaam karega)
st.sidebar.header("🔍 SELECT STOCK TO ANALYZE")
watchlist = ["RELIANCE.NS", "SBIN.NS", "SUNPHARMA.NS", "ZOMATO.NS", "TATAMOTORS.NS", "HAL.NS"]
selected_stock = st.sidebar.selectbox("Click/Select a Stock:", watchlist)

st.markdown(f"<h1>📈 Analyzing: {selected_stock}</h1>", unsafe_allow_html=True)

# 2. FETCH DATA
try:
    ticker = yf.Ticker(selected_stock)
    # 5-minute candles for detail view
    df = ticker.history(period='1d', interval='5m')
    info = ticker.fast_info
    
    if not df.empty:
        # 3. LIVE CANDLESTICK CHART
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

        # 4. QUICK DETAILS CARD
        c1, c2, c3 = st.columns(3)
        change = ((info['last_price'] - info['previous_close']) / info['previous_close']) * 100
        
        with c1:
            st.markdown(f"### Price: ₹{info['last_price']:.2f}")
            st.markdown(f"**Change:** {change:+.2f}%")
        with c2:
            st.markdown(f"### High/Low")
            st.markdown(f"H: ₹{info['day_high']:.2f} | L: ₹{info['day_low']:.2f}")
        with c3:
            # Simple RSI/Signal Logic
            st.markdown("### SIGNAL")
            signal = "STRONG BUY 🚀" if change > 1 else "WATCHING 👀" if abs(change) < 1 else "SELL 🔴"
            st.subheader(signal)

except:
    st.error("Data loading... Please wait.")

# Heatmap Summary (Niche dikhegi)
st.markdown("---")
st.caption("Tip: Use the sidebar to switch between stocks instantly for detailed analysis.")

time.sleep(10)
st.rerun()
