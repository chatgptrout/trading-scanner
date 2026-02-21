import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY EMA MOBILE", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem;}</style>""", unsafe_allow_html=True)

# --- 1. PCR STATUS (BADA AUR SAAF) ---
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

st.markdown(f"""
    <div style='background: #111; padding: 10px; border-radius: 8px; border: 2px solid {pcr_color}; text-align: center; margin-bottom: 5px;'>
        <h3 style='color: {pcr_color}; margin: 0; font-size: 20px;'>NIFTY PCR: {pcr_val}</h3>
        <p style='color: white; margin: 0; font-size: 12px; font-weight: bold;'>SENTIMENT: BEARISH ⚠️</p>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE BIG PRICE ---
df = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df.empty:
    ltp = df['Close'].iloc[-1]
    st.markdown(f"""
        <div style='text-align: center; background: #000; padding: 10px; border-radius: 10px;'>
            <h1 style='color: white; font-size: 50px; margin: 0;'>{ltp:,.2f}</h1>
            <p style='color: gray; font-size: 12px; margin: 0;'>NIFTY 50 LIVE SPOT</p>
        </div>
    """, unsafe_allow_html=True)

# --- 3. 5-MIN CHART WITH EMA 9 (BLUE) & 20 (YELLOW) ---
df_c = yf.Ticker("^NSEI").history(period="1d", interval="5m")
if not df_c.empty:
    df_c['EMA9'] = df_c['Close'].ewm(span=9, adjust=False).mean() # Blue
    df_c['EMA20'] = df_c['Close'].ewm(span=20, adjust=False).mean() # Yellow
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_c.index, open=df_c['Open'], high=df_c['High'], 
                               low=df_c['Low'], close=df_c['Close'], name='Price'))
    
    # Blue EMA 9 & Yellow EMA 20
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA9'], line=dict(color='#00d2ff', width=2), name='EMA 9'))
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA20'], line=dict(color='yellow', width=2.5), name='EMA 20'))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, height=450, 
        margin=dict(l=0, r=0, t=5, b=0), showlegend=False,
        yaxis=dict(tickformat='.2f', side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

time.sleep(10)
st.rerun()
