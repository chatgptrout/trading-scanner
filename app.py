import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Full Screen & No Padding Layout
st.set_page_config(page_title="NIFTY ULTIMATE PRO", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .block-container {padding: 0.5rem 1rem 0rem 1rem !important;}
    iframe {height: 400px !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. TOP BAR (PCR + WATCH) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 # Current
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

t1, t2 = st.columns([1, 6])
with t1:
    st.markdown(f"""
        <div style='text-align: center; background: #000; border-radius: 50%; width: 100px; height: 100px; 
                    margin: auto; border: 4px solid {pcr_color}; box-shadow: 0 0 15px {pcr_color};
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0; font-size: 28px;'>{pcr_val}</h2>
            <p style='color: {pcr_color}; margin: 0; font-size: 10px; font-weight: bold;'>PCR</p>
        </div>
        <div style='text-align: center; margin-top: 5px; background: {pcr_color}; color: white; 
                    padding: 2px; border-radius: 5px; font-size: 10px; font-weight: bold;'>SAVDHAN ⚠️</div>
    """, unsafe_allow_html=True)

with t2:
    # --- 2. PIVOT CHART (FIXED HEIGHT TO PREVENT CUTTING) ---
    df = yf.Ticker("^NSEI").history(period="2d", interval="5m")
    if len(df) > 0:
        last_day = yf.Ticker("^NSEI").history(period="2d")
        if len(last_day) > 1:
            # Pivot Calc
            ph, pl, pc = last_day['High'].iloc[-2], last_day['Low'].iloc[-2], last_day['Close'].iloc[-2]
            pp = (ph + pl + pc) / 3
            r1, s1 = (2 * pp) - pl, (2 * pp) - ph
            
            today_df = df[df.index.date == df.index.date[-1]]
            fig = go.Figure(data=[go.Candlestick(x=today_df.index, open=today_df['Open'], 
                            high=today_df['High'], low=today_df['Low'], close=today_df['Close'], name='Price')])
            
            # Pivot Lines
            fig.add_hline(y=pp, line_color="orange", annotation_text="PIVOT")
            fig.add_hline(y=r1, line_dash="dash", line_color="red", annotation_text="R1")
            fig.add_hline(y=s1, line_dash="dash", line_color="green", annotation_text="S1")
            
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=380, 
                              margin=dict(l=0, r=0, t=0, b=0), yaxis=dict(tickformat='.2f', side="right"))
            st.plotly_chart(fig, use_container_width=True)

# --- 3. BOTTOM PANEL (NO-CUT SPOT PRICE) ---
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    hi, lo = df_n['High'].max(), df_n['Low'].min()
    
    st.markdown(f"""
        <div style='background: #000; padding: 10px; border-radius: 12px; display: flex; 
                    justify-content: space-around; align-items: center; border: 2px solid #333; 
                    border-bottom: 5px solid {pcr_color}; margin-top: -20px;'>
            <div style='text-align: center;'>
                <p style='color: gray; margin: 0; font-size: 11px;'>NIFTY 50 SPOT</p>
                <h1 style='color: white; margin: 0; font-size: 42px; font-family: serif;'>{ltp:,.2f}</h1>
            </div>
            <div style='text-align: center;'>
                <p style='color: #00c853; margin: 0; font-size: 11px;'>SESSION HIGH</p>
                <h2 style='color: white; margin: 0; font-size: 28px;'>{hi:,.2f}</h2>
            </div>
            <div style='text-align: center;'>
                <p style='color: #ff1744; margin: 0; font-size: 11px;'>SESSION LOW</p>
                <h2 style='color: white; margin: 0; font-size: 28px;'>{lo:,.2f}</h2>
            </div>
            <div style='color: gray; font-size: 11px; text-align: right;'>⌚ {now.strftime('%I:%M:%S %p')}</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
