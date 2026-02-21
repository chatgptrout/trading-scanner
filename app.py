import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Page setup for 100% Screen Fit
st.set_page_config(page_title="NIFTY LIVE TERMINAL", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 1rem 0rem 1rem !important;}</style>""", unsafe_allow_html=True)

# --- 1. TOP BAR: MINIMAL PCR ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 # Current Signal
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

t1, t2 = st.columns([1, 8])
with t1:
    # Compact Circle (No cutting)
    st.markdown(f"""
        <div style='text-align: center; background: #000; border-radius: 50%; width: 70px; height: 70px; 
                    margin: auto; border: 4px solid {pcr_color}; box-shadow: 0 0 15px {pcr_color};
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0; font-size: 20px;'>{pcr_val}</h2>
            <p style='color: {pcr_color}; margin: 0; font-size: 7px; font-weight: bold;'>PCR</p>
        </div>
    """, unsafe_allow_html=True)

with t2:
    # --- 2. LIVE NIFTY CHART (ZOOMED) ---
    # Fetching real-time data
    df = yf.Ticker("^NSEI").history(period="1d", interval="1m") # 1m for ultra-live feel
    if not df.empty:
        df['MA20'] = df['Close'].rolling(window=20).mean() # Yellow Trend Line
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                   low=df['Low'], close=df['Close'], name='Live Price'))
        
        # Yellow Line
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=3)))
        
        current_p = df['Close'].iloc[-1]
        fig.update_layout(
            template="plotly_dark", xaxis_rangeslider_visible=False, height=450, 
            margin=dict(l=0, r=0, t=5, b=0),
            yaxis=dict(tickformat='.2f', side="right", range=[current_p - 100, current_p + 100])
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 3. BOTTOM PANEL: FULL BOLD NUMBERS ---
# Displaying spot price with zero shortcuts
if not df.empty:
    ltp = df['Close'].iloc[-1]
    st.markdown(f"""
        <div style='background: #000; padding: 12px; border-radius: 10px; display: flex; 
                    justify-content: space-between; align-items: center; border-bottom: 5px solid {pcr_color};'>
            <div style='flex: 2; text-align: center;'>
                <p style='color: gray; margin: 0; font-size: 11px;'>NIFTY 50 LIVE</p>
                <h1 style='color: white; margin: 0; font-size: 50px; font-family: serif;'>{ltp:,.2f}</h1>
            </div>
            <div style='flex: 1; text-align: center; border-left: 1px solid #333;'>
                <p style='color: #00c853; margin: 0; font-size: 11px;'>HIGH TODAY</p>
                <h2 style='color: white; margin: 0;'>{df['High'].max():,.2f}</h2>
            </div>
            <div style='flex: 1; text-align: right; color: gray; font-size: 11px;'>
                ⌚ {now.strftime('%I:%M:%S %p')}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh every 10 seconds to keep it live
time.sleep(10)
st.rerun()
