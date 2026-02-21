import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Full Screen & Compact Margin
st.set_page_config(page_title="NIFTY ZOOM PRO", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>.block-container {padding: 0.5rem 1rem 0rem 1rem !important;}</style>""", unsafe_allow_html=True)

# --- 1. TOP BAR (PCR & CLOCK) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
pcr_val = 2.01 #
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"

t1, t2 = st.columns([1, 6])
with t1:
    st.markdown(f"""
        <div style='text-align: center; background: #000; border-radius: 50%; width: 85px; height: 85px; 
                    margin: auto; border: 4px solid {pcr_color}; box-shadow: 0 0 15px {pcr_color};
                    display: flex; flex-direction: column; justify-content: center;'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>{pcr_val}</h2>
            <p style='color: {pcr_color}; margin: 0; font-size: 8px; font-weight: bold;'>PCR</p>
        </div>
    """, unsafe_allow_html=True)

with t2:
    # --- 2. THE ZOOMED CHART (CANDLES + TREND) ---
    df = yf.Ticker("^NSEI").history(period="2d", interval="5m")
    if len(df) > 0:
        # Pivot Calculations
        last_day = yf.Ticker("^NSEI").history(period="2d")
        ph, pl, pc = last_day['High'].iloc[-2], last_day['Low'].iloc[-2], last_day['Close'].iloc[-2]
        pp = (ph + pl + pc) / 3
        
        today_df = df[df.index.date == df.index.date[-1]].copy()
        today_df['MA20'] = today_df['Close'].rolling(window=20).mean() # Yellow Trend Line

        fig = go.Figure()
        
        # Candles with Increased Width for Zoom Effect
        fig.add_trace(go.Candlestick(
            x=today_df.index, open=today_df['Open'], high=today_df['High'], 
            low=today_df['Low'], close=today_df['Close'], name='Price'
        ))
        
        # YELLOW TREND LINE (Bold)
        fig.add_trace(go.Scatter(x=today_df.index, y=today_df['MA20'], name='Trend', 
                                 line=dict(color='yellow', width=3))) 
        
        # PIVOT Line
        fig.add_hline(y=pp, line_color="orange", opacity=0.6, annotation_text="PIVOT")
        
        # --- ZOOM LOGIC: Focus on Current Price Range ---
        current_price = today_df['Close'].iloc[-1]
        fig.update_layout(
            template="plotly_dark", 
            xaxis_rangeslider_visible=False, 
            height=400, 
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(
                tickformat='.2f', 
                side="right",
                range=[current_price - 150, current_price + 150] # AUTO ZOOM around price
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 3. BOTTOM PANEL (FULL NUMBERS) ---
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    st.markdown(f"""
        <div style='background: #000; padding: 10px; border-radius: 12px; display: flex; 
                    justify-content: space-around; align-items: center; border-bottom: 5px solid {pcr_color};'>
            <div style='text-align: center;'>
                <p style='color: gray; margin: 0; font-size: 11px;'>NIFTY 50 SPOT</p>
                <h1 style='color: white; margin: 0; font-size: 40px;'>{ltp:,.2f}</h1>
            </div>
            <div style='text-align: center; border-left: 1px solid #333; padding-left: 20px;'>
                <p style='color: #00c853; margin: 0; font-size: 11px;'>SESSION HIGH</p>
                <h2 style='color: white; margin: 0;'>{df_n['High'].max():,.2f}</h2>
            </div>
            <div style='color: gray; font-size: 11px;'>⌚ {now.strftime('%I:%M:%S %p')}</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
