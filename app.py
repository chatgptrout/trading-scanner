import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Mobile Layout Optimization
st.set_page_config(page_title="NIFTY EMA PRO", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem;}</style>""", unsafe_allow_html=True)

# --- 1. NEW COMPACT PCR BAR (NO CUTTING) ---
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

st.markdown(f"""
    <div style='background: #111; padding: 10px; border-radius: 10px; border-left: 5px solid {pcr_color}; margin-bottom: 10px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='color: gray; font-size: 14px;'>NIFTY PCR SENTIMENT</span>
            <span style='color: {pcr_color}; font-size: 24px; font-weight: bold;'>{pcr_val}</span>
        </div>
        <div style='background: {pcr_color}; height: 4px; border-radius: 2px; margin-top: 5px; width: {pcr_val*30}%'></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. LIVE NIFTY PRICE ---
df = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df.empty:
    ltp = df['Close'].iloc[-1]
    st.markdown(f"""
        <div style='text-align: center; background: #000; padding: 10px; border-radius: 10px;'>
            <h1 style='color: white; font-size: 40px; margin: 0;'>{ltp:,.2f}</h1>
            <p style='color: {pcr_color}; font-weight: bold; margin: 0;'>AI SIGNAL: {'BEARISH ⚠️' if pcr_val > 1.5 else 'BULLISH ✅'}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 3. CHART WITH EMA 9/20 ---
df_c = yf.Ticker("^NSEI").history(period="1d", interval="5m")
if not df_c.empty:
    # EMA Calculation
    df_c['EMA9'] = df_c['Close'].ewm(span=9, adjust=False).mean()
    df_c['EMA20'] = df_c['Close'].ewm(span=20, adjust=False).mean()
    
    fig = go.Figure()
    # Candles
    fig.add_trace(go.Candlestick(x=df_c.index, open=df_c['Open'], high=df_c['High'], 
                               low=df_c['Low'], close=df_c['Close'], name='Price'))
    
    # Blue Line (9 EMA) - Fast
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA9'], line=dict(color='#00d2ff', width=1.5), name='EMA 9'))
    # Yellow Line (20 EMA) - Slow
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA20'], line=dict(color='yellow', width=2), name='EMA 20'))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, height=400, 
        margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
        yaxis=dict(tickformat='.2f', side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. QUICK STATS ---
st.markdown(f"<p style='text-align:center; color:gray; font-size:10px;'>HIGH: {df['High'].max():,.2f} | LOW: {df['Low'].min():,.2f} | ⌚ {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
