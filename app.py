import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY PIVOT MOBILE", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem;}</style>""", unsafe_allow_html=True)

# --- 1. THE BIG PRICE (TOP FOCUS) ---
df_live = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_live.empty:
    ltp = df_live['Close'].iloc[-1]
    st.markdown(f"""
        <div style='text-align: center; background: #000; padding: 10px; border-radius: 10px; border-bottom: 3px solid #333;'>
            <h1 style='color: white; font-size: 45px; margin: 0;'>{ltp:,.2f}</h1>
            <p style='color: gray; font-size: 11px; margin: 0;'>NIFTY 50 LIVE SPOT</p>
        </div>
    """, unsafe_allow_html=True)

# --- 2. 5-MIN CHART WITH EMA & PIVOT POINTS ---
df_c = yf.Ticker("^NSEI").history(period="2d", interval="5m") # 2 days for pivot
if not df_c.empty:
    # EMA Calculation
    df_c['EMA9'] = df_c['Close'].ewm(span=9, adjust=False).mean()
    df_c['EMA20'] = df_c['Close'].ewm(span=20, adjust=False).mean()
    
    # Pivot Point Calculation
    last_day = yf.Ticker("^NSEI").history(period="2d")
    ph, pl, pc = last_day['High'].iloc[-2], last_day['Low'].iloc[-2], last_day['Close'].iloc[-2]
    pp = (ph + pl + pc) / 3
    r1, s1 = (2 * pp) - pl, (2 * pp) - ph
    
    today_df = df_c[df_c.index.date == df_c.index.date[-1]].copy()
    
    fig = go.Figure()
    # Candles
    fig.add_trace(go.Candlestick(x=today_df.index, open=today_df['Open'], high=today_df['High'], 
                               low=today_df['Low'], close=today_df['Close'], name='Price'))
    
    # EMA 9 (Blue) & EMA 20 (Yellow)
    fig.add_trace(go.Scatter(x=today_df.index, y=today_df['EMA9'], line=dict(color='#00d2ff', width=1.5), name='EMA 9'))
    fig.add_trace(go.Scatter(x=today_df.index, y=today_df['EMA20'], line=dict(color='yellow', width=2), name='EMA 20'))
    
    # Pivot Points (R1 & S1)
    fig.add_hline(y=r1, line_dash="dash", line_color="red", opacity=0.6, annotation_text="R1")
    fig.add_hline(y=s1, line_dash="dash", line_color="green", opacity=0.6, annotation_text="S1")
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, height=400, 
        margin=dict(l=0, r=0, t=5, b=0), showlegend=False,
        yaxis=dict(tickformat='.2f', side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 3. PCR STATUS (SHIFTED TO BOTTOM) ---
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"
st.markdown(f"""
    <div style='background: #111; padding: 10px; border-radius: 8px; border-left: 8px solid {pcr_color}; margin-top: 10px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='color: white; font-size: 14px; font-weight: bold;'>PCR SENTIMENT</span>
            <span style='color: {pcr_color}; font-size: 22px; font-weight: bold;'>{pcr_val}</span>
        </div>
        <p style='color: {pcr_color}; margin: 0; font-size: 11px; font-weight: bold;'>AI SIGNAL: {'BEARISH ⚠️' if pcr_val > 1.5 else 'BULLISH ✅'}</p>
    </div>
""", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
