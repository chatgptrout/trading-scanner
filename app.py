import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Page setup for minimal padding
st.set_page_config(page_title="NIFTY COMPACT", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding-top: 1rem; padding-bottom: 0rem;}</style>""", unsafe_allow_html=True)

# --- 1. COMPACT TOP BAR ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
t1, t2, t3 = st.columns([2, 5, 2])

with t1:
    # Small Glowing PCR
    pcr_val = 2.01
    pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"
    st.markdown(f"""
        <div style='border: 2px solid {pcr_color}; border-radius: 10px; padding: 5px; text-align: center; background: #000; box-shadow: 0 0 10px {pcr_color};'>
            <span style='color: gray; font-size: 12px;'>PCR:</span>
            <span style='color: white; font-size: 20px; font-weight: bold;'> {pcr_val}</span>
            <div style='color: {pcr_color}; font-size: 10px; font-weight: bold;'>SAVDHAN ⚠️</div>
        </div>
    """, unsafe_allow_html=True)

with t2:
    # Full Nifty Price - No Shortcuts
    df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
    if not df_n.empty:
        ltp = df_n['Close'].iloc[-1]
        price_full = "{:,.2f}".format(ltp)
        st.markdown(f"""
            <div style='text-align: center; background: #111; border-radius: 10px; padding: 5px; border-bottom: 3px solid {pcr_color};'>
                <span style='color: gray; font-size: 12px;'>NIFTY 50: </span>
                <span style='color: white; font-size: 32px; font-weight: bold;'>{price_full}</span>
            </div>
        """, unsafe_allow_html=True)

with t3:
    st.markdown(f"<p style='text-align:right; color:gray; font-size: 12px;'>⌚ {now.strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)

# --- 2. THE MAIN CHART (FULL WIDTH) ---
# High precision candle view
df_c = yf.Ticker("^NSEI").history(period="1d", interval="5m")
if not df_c.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df_c.index, open=df_c['Open'], high=df_c['High'], 
        low=df_c['Low'], close=df_c['Close'], name='Nifty'
    )])
    df_c['MA20'] = df_c['Close'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['MA20'], name='Trend', line=dict(color='yellow', width=1.5)))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, 
        height=550, margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(tickformat='.2f', side="right") # Full numbers on Y axis
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 3. BOTTOM QUICK STATS ---
if not df_n.empty:
    hi, lo = df_n['High'].max(), df_n['Low'].min()
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; background: #000; padding: 5px; border-radius: 5px; border: 1px solid #333;'>
            <div style='color: #00c853; font-size: 14px;'><b>BULLISH ></b> {hi:,.2f}</div>
            <div style='color: #ff1744; font-size: 14px;'><b>BEARISH <</b> {lo:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
