import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

# Page configuration
st.set_page_config(page_title="NIFTY DESI POWER", layout="wide")

# --- 1. THE WATCH ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3 style='color:#888;'>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. GLOWING PCR CIRCLE (PURE DESI STYLE) ---
pcr_val = 2.01 # Latest data
# Red for Danger (>1.5), Green for Mauj (<1.0)
pcr_color = "#ff0033" if pcr_val > 1.5 else "#00ff66"
glow_style = f"box-shadow: 0 0 50px {pcr_color}, inset 0 0 20px {pcr_color};"

st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 40px;'>
        <div style='width: 280px; height: 280px; border-radius: 50%; border: 8px solid {pcr_color}; 
                    display: flex; justify-content: center; align-items: center; background: #000;
                    {glow_style}'>
            <div style='text-align: center;'>
                <h1 style='color: white; font-size: 85px; margin: 0; font-family: sans-serif;'>{pcr_val}</h1>
                <p style='color: {pcr_color}; font-size: 18px; font-weight: bold; margin: 0; letter-spacing: 2px;'>NIFTY PCR</p>
            </div>
        </div>
        <div style='margin-top: 30px; background: {pcr_color}; color: white; padding: 12px 60px; 
                    border-radius: 50px; font-size: 28px; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>
            {'BEARISH: SAVDHAN ⚠️' if pcr_val > 1.5 else 'BULLISH: MAUJ ✅'}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. NIFTY 50 LIVE CANDLES (CLEAN VIEW) ---
st.markdown("<br>## 🕯️ NIFTY 50 (REAL-TIME PRICE ACTION)")

def draw_nifty_clean():
    df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close'], name='Price'
        )])
        
        # Yellow Trend Line (MA20)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=2)))
        
        # Formatting Y-axis to avoid '25k' - Hardcoded
        fig.update_layout(
            template="plotly_dark", 
            xaxis_rangeslider_visible=False, 
            height=500,
            yaxis=dict(tickformat='.2f', title="Price (No Shortcuts)")
        )
        st.plotly_chart(fig, use_container_width=True)

draw_nifty_clean()

# --- 4. THE SPOT PRICE (ULTRA BOLD - NO SHORTCUTS) ---
st.markdown("---")
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    # Forced formatting: 25565.90 style
    price_full = "{:,.2f}".format(ltp)
    hi_full = "{:,.2f}".format(df_n['High'].max())
    lo_full = "{:,.2f}".format(df_n['Low'].min())
    
    st.markdown(f"""
        <div style='background: #000; padding: 50px; border-radius: 25px; text-align: center; border: 4px solid {pcr_color};'>
            <h2 style='color: #888; margin: 0; font-family: monospace;'>NIFTY 50 SPOT PRICE</h2>
            <h1 style='color: white; font-size: 120px; margin: 15px 0; font-family: serif; letter-spacing: -2px;'>{price_full}</h1>
            <div style='display: flex; justify-content: center; gap: 80px; border-top: 1px solid #333; padding-top: 20px;'>
                <div>
                    <p style='color: #00c853; font-size: 18px; margin: 0;'>BULLISH ABOVE</p>
                    <h2 style='color: white; margin: 0;'>{hi_full}</h2>
                </div>
                <div>
                    <p style='color: #ff1744; font-size: 18px; margin: 0;'>BEARISH BELOW</p>
                    <h2 style='color: white; margin: 0;'>{lo_full}</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
