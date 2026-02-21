import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Page config for ultra-clean look
st.set_page_config(page_title="NIFTY S/R COMPACT", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 1rem 1rem 0rem 1rem; background-color: #ffffff;}</style>""", unsafe_allow_html=True)

# --- 1. TOP SECTION: PCR & CLOCK ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 # Current
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

t1, t2 = st.columns([1, 5])
with t1:
    # Small Glowing PCR Circle
    st.markdown(f"""
        <div style='text-align: center;'>
            <div style='width: 120px; height: 120px; border-radius: 50%; border: 5px solid {pcr_color}; 
                        display: flex; flex-direction: column; justify-content: center; align-items: center; 
                        background: #000; box-shadow: 0 0 20px {pcr_color};'>
                <h2 style='color: white; margin: 0; font-size: 35px;'>{pcr_val}</h2>
                <p style='color: {pcr_color}; margin: 0; font-size: 10px; font-weight: bold;'>PCR</p>
            </div>
            <div style='margin-top: 10px; background: {pcr_color}; color: white; padding: 2px 10px; 
                        border-radius: 10px; font-size: 11px; font-weight: bold;'>SAVDHAN ⚠️</div>
        </div>
    """, unsafe_allow_html=True)

with t2:
    # --- 2. THE MAIN CHART WITH S/R LINES ---
    df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    if not df.empty:
        hi_val, lo_val = df['High'].max(), df['Low'].min()
        
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close'], name='Price'
        )])
        
        # Yellow Trend Line
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=2)))
        
        # Permanent S/R Lines
        fig.add_hline(y=hi_val, line_dash="dash", line_color="red", annotation_text="RESISTANCE", annotation_position="top left")
        fig.add_hline(y=lo_val, line_dash="dash", line_color="green", annotation_text="SUPPORT", annotation_position="bottom left")
        
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, 
            height=450, margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(tickformat='.2f', side="right") # Full numbers
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 3. THE SLEEK BOTTOM BAR (NO SHORTCUTS) ---
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    price_full = "{:,.2f}".format(ltp)
    hi_full = "{:,.2f}".format(df_n['High'].max())
    lo_full = "{:,.2f}".format(df_n['Low'].min())
    
    st.markdown(f"""
        <div style='background: #000; padding: 15px; border-radius: 10px; display: flex; 
                    justify-content: space-around; align-items: center; border-left: 10px solid {pcr_color};'>
            <div style='text-align: center;'>
                <p style='color: gray; margin: 0; font-size: 10px;'>NIFTY 50 SPOT</p>
                <h1 style='color: white; margin: 0; font-size: 35px;'>{price_full}</h1>
            </div>
            <div style='text-align: center;'>
                <p style='color: #00c853; margin: 0; font-size: 10px;'>BULLISH ABOVE</p>
                <h2 style='color: white; margin: 0;'>{hi_full}</h2>
            </div>
            <div style='text-align: center;'>
                <p style='color: #ff1744; margin: 0; font-size: 10px;'>BEARISH BELOW</p>
                <h2 style='color: white; margin: 0;'>{lo_full}</h2>
            </div>
            <div style='text-align: right; color: gray; font-size: 10px;'>⌚ {now.strftime('%I:%M:%S %p')}</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
