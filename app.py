import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Mobile Optimization: No Sidebar, Tight Padding
st.set_page_config(page_title="NIFTY MOBILE AI", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem;}</style>""", unsafe_allow_html=True)

# --- 1. MOBILE HEADER ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

# Big PCR Circle for Mobile
st.markdown(f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <div style='width: 100px; height: 100px; border-radius: 50%; border: 5px solid {pcr_color}; 
                    margin: auto; display: flex; flex-direction: column; justify-content: center; background: #000;'>
            <h1 style='color: white; font-size: 30px; margin: 0;'>{pcr_val}</h1>
            <p style='color: {pcr_color}; font-size: 10px; font-weight: bold; margin: 0;'>PCR</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. LIVE NIFTY PRICE (BIG NUMBERS) ---
df = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df.empty:
    ltp = df['Close'].iloc[-1]
    price_full = "{:,.2f}".format(ltp) # No 25k Shortcut
    
    # --- AI SMART ALERT LOGIC ---
    # Buy if Price > Yellow Line, Sell if PCR High
    ai_msg = "SELL / WAIT ⚠️" if pcr_val > 1.5 else "BUY / HOLD ✅"
    
    st.markdown(f"""
        <div style='background: #000; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid {pcr_color};'>
            <h1 style='color: white; font-size: 45px; margin: 0;'>{price_full}</h1>
            <div style='background: {pcr_color}; color: white; padding: 5px; border-radius: 5px; font-weight: bold; font-size: 20px; margin-top: 10px;'>
                {ai_msg}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 3. MOBILE CHART (ZOOMED) ---
st.markdown("<p style='text-align:center; color:gray; font-size:12px; margin-top:10px;'>LIVE CANDLESTICK TREND</p>", unsafe_allow_html=True)
df_c = yf.Ticker("^NSEI").history(period="1d", interval="5m")
if not df_c.empty:
    df_c['MA20'] = df_c['Close'].rolling(window=20).mean() # Yellow Trend Line
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_c.index, open=df_c['Open'], high=df_c['High'], 
                               low=df_c['Low'], close=df_c['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['MA20'], line=dict(color='yellow', width=2), name='Trend'))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, height=350, 
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(tickformat='.2f', side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. BOTTOM STATS (CLEAN) ---
st.markdown(f"""
    <div style='display: flex; justify-content: space-around; color: gray; font-size: 12px; margin-top: 10px;'>
        <span>HIGH: {df['High'].max():,.2f}</span>
        <span>LOW: {df['Low'].min():,.2f}</span>
        <span>⌚ {now.strftime('%I:%M %p')}</span>
    </div>
""", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
