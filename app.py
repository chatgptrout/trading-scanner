import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY COMPACT PRO", layout="wide")

# --- 1. COMPACT HEADER & WATCH ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
h1, h2 = st.columns([8, 2])
with h2:
    st.markdown(f"<p style='text-align:right; color:gray; margin:0;'>⌚ {now.strftime('%I:%M:%S %p')}</p>", unsafe_allow_html=True)

# --- 2. PCR & NIFTY CHART (SIDE BY SIDE FOR SPACE) ---
pcr_val = 2.01 
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

col_left, col_right = st.columns([1, 4]) # Chart gets 80% space

with col_left:
    # Compact Glowing PCR Circle
    st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;'>
            <div style='width: 160px; height: 160px; border-radius: 50%; border: 6px solid {pcr_color}; 
                        display: flex; justify-content: center; align-items: center; background: #000;
                        box-shadow: 0 0 30px {pcr_color};'>
                <div style='text-align: center;'>
                    <h1 style='color: white; font-size: 45px; margin: 0;'>{pcr_val}</h1>
                    <p style='color: {pcr_color}; font-size: 12px; font-weight: bold; margin: 0;'>PCR</p>
                </div>
            </div>
            <div style='margin-top: 15px; background: {pcr_color}; color: white; padding: 5px 20px; 
                        border-radius: 20px; font-size: 14px; font-weight: bold;'>SAVDHAN ⚠️</div>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # High Clarity Candle Graph
    df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close'], name='Price'
        )])
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=2)))
        
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, 
            height=450, margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(tickformat='.2f', side="right") # Price on right for better view
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 3. FLOATING PRICE BAR (NO 25K SHORTCUT) ---
st.markdown("---")
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    # Forced full number formatting
    price_full = "{:,.2f}".format(ltp)
    hi_val = "{:,.2f}".format(df_n['High'].max())
    lo_val = "{:,.2f}".format(df_n['Low'].min())
    
    st.markdown(f"""
        <div style='background: #000; padding: 15px; border-radius: 10px; display: flex; 
                    justify-content: space-around; align-items: center; border-left: 10px solid {pcr_color};'>
            <div style='text-align: left;'>
                <p style='color: gray; margin: 0; font-size: 12px;'>NIFTY 50 SPOT</p>
                <h1 style='color: white; margin: 0; font-size: 40px;'>{price_full}</h1>
            </div>
            <div style='text-align: center;'>
                <p style='color: #00c853; margin: 0; font-size: 12px;'>BULLISH ABOVE</p>
                <h3 style='color: white; margin: 0;'>{hi_val}</h3>
            </div>
            <div style='text-align: center;'>
                <p style='color: #ff1744; margin: 0; font-size: 12px;'>BEARISH BELOW</p>
                <h3 style='color: white; margin: 0;'>{lo_val}</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
