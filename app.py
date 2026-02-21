import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY EMA MOBILE", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 0.5rem;}</style>""", unsafe_allow_html=True)

# --- 1. NEW TOP PCR STATUS BAR (VISIBLE & CLEAR) ---
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

st.markdown(f"""
    <div style='background: #111; padding: 12px; border-radius: 8px; border-bottom: 4px solid {pcr_color}; margin-bottom: 5px;'>
        <div style='display: flex; justify-content: space-between;'>
            <span style='color: white; font-weight: bold;'>PCR: {pcr_val}</span>
            <span style='color: {pcr_color}; font-weight: bold;'>{'⚠️ BEARISH' if pcr_val > 1.5 else '✅ BULLISH'}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE BIG PRICE & AI SIGNAL ---
df = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df.empty:
    ltp = df['Close'].iloc[-1]
    st.markdown(f"""
        <div style='text-align: center; background: #000; padding: 15px; border-radius: 10px; border: 1px solid #333;'>
            <h1 style='color: white; font-size: 48px; margin: 0;'>{ltp:,.2f}</h1>
            <p style='color: gray; font-size: 12px; margin: 0;'>NIFTY 50 LIVE SPOT</p>
        </div>
    """, unsafe_allow_html=True)

# --- 3. 5-MIN CHART WITH EMA 9 (BLUE) & 20 (YELLOW) ---
df_c = yf.Ticker("^NSEI").history(period="1d", interval="5m")
if not df_c.empty:
    df_c['EMA9'] = df_c['Close'].ewm(span=9, adjust=False).mean() # Blue Line
    df_c['EMA20'] = df_c['Close'].ewm(span=20, adjust=False).mean() # Yellow Line
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_c.index, open=df_c['Open'], high=df_c['High'], 
                               low=df_c['Low'], close=df_c['Close'], name='Price'))
    
    # Blue Fast EMA
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA9'], line=dict(color='#00d2ff', width=2), name='EMA 9'))
    # Yellow Slow EMA
    fig.add_trace(go.Scatter(x=df_c.index, y=df_c['EMA20'], line=dict(color='yellow', width=2.5), name='EMA 20'))
    
    fig.update_layout(
        template="plotly_dark", xaxis_rangeslider_visible=False, height=450, 
        margin=dict(l=0, r=0, t=5, b=0), showlegend=False,
        yaxis=dict(tickformat='.2f', side="right")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. BOTTOM QUICK VIEW ---
st.markdown(f"<p style='text-align:center; color:gray; font-size:11px;'>H: {df['High'].max():,.2f} | L: {df['Low'].min():,.2f} | ⌚ {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
