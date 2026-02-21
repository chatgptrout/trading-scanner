import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Page config for high-precision view
st.set_page_config(page_title="NIFTY PIVOT PRO", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 1rem 1rem 0rem 1rem; background-color: #ffffff;}</style>""", unsafe_allow_html=True)

# --- 1. TOP SECTION: PCR & CLOCK ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 # Current
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

t1, t2 = st.columns([1, 5])
with t1:
    st.markdown(f"""
        <div style='text-align: center;'>
            <div style='width: 110px; height: 110px; border-radius: 50%; border: 5px solid {pcr_color}; 
                        display: flex; flex-direction: column; justify-content: center; align-items: center; 
                        background: #000; box-shadow: 0 0 15px {pcr_color};'>
                <h2 style='color: white; margin: 0; font-size: 30px;'>{pcr_val}</h2>
                <p style='color: {pcr_color}; margin: 0; font-size: 10px; font-weight: bold;'>PCR</p>
            </div>
            <div style='margin-top: 8px; background: {pcr_color}; color: white; padding: 2px 8px; 
                        border-radius: 8px; font-size: 10px; font-weight: bold;'>SAVDHAN ⚠️</div>
        </div>
    """, unsafe_allow_html=True)

with t2:
    # --- 2. CHART WITH PIVOT POINTS ---
    df = yf.Ticker("^NSEI").history(period="2d", interval="5m") # 2 days data needed for pivots
    if len(df) > 0:
        # Pivot Point Calculation (Standard)
        last_day = yf.Ticker("^NSEI").history(period="2d")
        if len(last_day) > 1:
            prev_high = last_day['High'].iloc[-2]
            prev_low = last_day['Low'].iloc[-2]
            prev_close = last_day['Close'].iloc[-2]
            
            pivot = (prev_high + prev_low + prev_close) / 3
            r1 = (2 * pivot) - prev_low
            s1 = (2 * pivot) - prev_high
            r2 = pivot + (prev_high - prev_low)
            s2 = pivot - (prev_high - prev_low)

            today_df = df[df.index.date == df.index.date[-1]]
            
            fig = go.Figure(data=[go.Candlestick(
                x=today_df.index, open=today_df['Open'], high=today_df['High'], 
                low=today_df['Low'], close=today_df['Close'], name='Price'
            )])
            
            # Pivot Lines
            fig.add_hline(y=pivot, line_dash="solid", line_color="orange", annotation_text="PIVOT")
            fig.add_hline(y=r1, line_dash="dash", line_color="red", annotation_text="R1")
            fig.add_hline(y=s1, line_dash="dash", line_color="green", annotation_text="S1")
            fig.add_hline(y=r2, line_dash="dot", line_color="darkred", annotation_text="R2")
            
            fig.update_layout(
                template="plotly_dark", xaxis_rangeslider_visible=False, 
                height=420, margin=dict(l=0, r=0, t=0, b=0),
                yaxis=dict(tickformat='.2f', side="right") # Full numbers
            )
            st.plotly_chart(fig, use_container_width=True)

# --- 3. BOTTOM BAR (FULL PRECISION) ---
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    st.markdown(f"""
        <div style='background: #000; padding: 12px; border-radius: 8px; display: flex; 
                    justify-content: space-around; align-items: center; border-left: 8px solid {pcr_color};'>
            <div style='text-align: center;'>
                <p style='color: gray; margin: 0; font-size: 10px;'>NIFTY 50 SPOT</p>
                <h1 style='color: white; margin: 0; font-size: 32px;'>{ltp:,.2f}</h1>
            </div>
            <div style='text-align: center;'>
                <p style='color: #00c853; margin: 0; font-size: 10px;'>SESSION HIGH</p>
                <h3 style='color: white; margin: 0;'>{df_n['High'].max():,.2f}</h3>
            </div>
            <div style='text-align: center;'>
                <p style='color: #ff1744; margin: 0; font-size: 10px;'>SESSION LOW</p>
                <h3 style='color: white; margin: 0;'>{df_n['Low'].min():,.2f}</h3>
            </div>
            <div style='color: gray; font-size: 10px;'>⌚ {now.strftime('%I:%M:%S %p')}</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
