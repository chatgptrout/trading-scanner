import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY DESI POWER", layout="wide")

# --- 1. THE WATCH ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3 style='color:#888;'>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. DESI PCR CIRCLE (BIG & BOLD) ---
pcr_val = 2.01 # Current
# Desi Logic: 1.5 se upar matlab Khatra (Red), 1.0 se niche matlab Mauj (Green)
pcr_color = "#ff1744" if pcr_val > 1.5 else "#00c853" 

st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 20px;'>
        <div style='width: 300px; height: 300px; border-radius: 50%; border: 15px solid {pcr_color}; 
                    display: flex; justify-content: center; align-items: center; background: #111;
                    box-shadow: 0 0 30px {pcr_color};'>
            <div style='text-align: center;'>
                <h1 style='color: white; font-size: 70px; margin: 0;'>{pcr_val}</h1>
                <p style='color: {pcr_color}; font-weight: bold; margin: 0;'>NIFTY PCR</p>
            </div>
        </div>
        <div style='margin-top: 20px; background: {pcr_color}; color: white; padding: 10px 40px; 
                    border-radius: 50px; font-size: 24px; font-weight: bold;'>
            {'BEARISH: SAVDHAN ⚠️' if pcr_val > 1.5 else 'BULLISH: MAUJ ✅'}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. NIFTY 50 LIVE ANALYSIS (FULL NUMBERS) ---
st.markdown("<br>## 🕯️ NIFTY 50 (NO SHORTCUTS - FULL PRICE)")

def draw_nifty_desi():
    df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    if not df.empty:
        # MACD & Trend
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal']

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
        
        # Candles
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                   low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
        
        # Trend Line
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=2)), row=1, col=1)
        
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

draw_nifty_desi()

# --- 4. SPOT PRICE (BADA BADA PRICE) ---
st.markdown("---")
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    # Formatting to ensure NO '25K' - only full numbers
    price_full = "{:,.2f}".format(ltp)
    
    st.markdown(f"""
        <div style='background: #000; padding: 40px; border-radius: 20px; text-align: center; border: 3px solid {pcr_color};'>
            <h2 style='color: gray; margin: 0;'>NIFTY 50 SPOT PRICE</h2>
            <h1 style='color: white; font-size: 100px; margin: 10px 0;'>{price_full}</h1>
            <div style='display: flex; justify-content: center; gap: 60px;'>
                <h2 style='color: #00c853;'>BULLISH > {df_n['High'].max():,.2f}</h2>
                <h2 style='color: #ff1744;'>BEARISH < {df_n['Low'].min():,.2f}</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
