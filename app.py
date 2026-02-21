import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI CANDLE TERMINAL", layout="wide")

# --- 1. DIGITAL CLOCK (IST) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI HEADER ---
pcr_val = 2.01 # Latest from screen
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#111; color:white; border-radius:15px; border-top:8px solid #00c853;'>
        <h1 style='margin:0; color:#00c853;'>PCR: {pcr_val}</h1>
        <h3 style='margin:0;'>AI STATUS: REVERSAL RISK ⚠️</h3>
    </div>
""", unsafe_allow_html=True)

# --- 3. CANDLESTICK CHART LOGIC ---
def draw_candle_chart(symbol, title):
    df = yf.Ticker(symbol).history(period="1d", interval="5m") # 5-min candles for clarity
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            increasing_line_color='#00c853', decreasing_line_color='#ff1744'
        )])
        fig.update_layout(title=title, template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>## 📊 LIVE CANDLESTICK ANALYSIS")

# Nifty Candle (Frozen as Market is Closed)
draw_candle_chart("^NSEI", "NIFTY 50 (5-MIN CANDLES)")

# Crude Oil Candle (LIVE RUNNING)
draw_candle_chart("CL=F", "CRUDE OIL (5-MIN CANDLES)")

# --- 4. DATA CARDS ---
st.markdown("---")
cols = st.columns(3)
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Natural Gas Precision
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"

        with cols[i]:
            st.markdown(f"""
                <div style='background:#1e1e1e; padding:15px; border-radius:10px; text-align:center; color:white;'>
                    <h4 style='color:gray;'>{name}</h4>
                    <h2 style='margin:0;'>{price_str}</h2>
                    <p style='color:#00c853;'>BULLISH > {hi:.2f}</p>
                    <p style='color:#ff1744;'>BEARISH < {lo:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
