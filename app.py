import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY AI ULTIMATE", layout="wide")

# --- 1. DIGITAL CLOCK (TOP RIGHT) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3 style='color:#888;'>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. DYNAMIC PCR CIRCLE (BEAUTIFUL GAUGE) ---
pcr_val = 2.01 # Latest
# Color Logic: Bullish (Green) if PCR < 1.0, Bearish (Red) if PCR > 1.5
pcr_color = "#ff1744" if pcr_val > 1.5 else "#00c853" 

fig_pcr = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = pcr_val,
    title = {'text': "NIFTY PCR (SENTIMENT)", 'font': {'size': 24}},
    gauge = {
        'axis': {'range': [None, 3], 'tickwidth': 1},
        'bar': {'color': pcr_color},
        'steps': [
            {'range': [0, 1], 'color': "#e8f5e9"},
            {'range': [1, 3], 'color': "#ffebee"}],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': pcr_val}}))

fig_pcr.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="#0e1117", font={'color': "white"})
st.plotly_chart(fig_pcr, use_container_width=True)

# AI Signal Alert
st.markdown(f"""
    <div style='text-align:center; padding:10px; background:{pcr_color}; color:white; border-radius:10px; font-weight:bold;'>
        AI STATUS: {'REVERSAL RISK ⚠️' if pcr_val > 1.5 else 'BULLISH MOMENTUM ✅'}
    </div>
""", unsafe_allow_html=True)

# --- 3. NIFTY 50 LIVE ANALYSIS (CANDLES + MACD) ---
st.markdown("<br>## ⚡ NIFTY 50 LIVE ANALYSIS (5-MIN CANDLES)")

def draw_nifty_chart():
    df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    if not df.empty:
        # MACD Calc
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal']

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
        
        # Candles
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
        
        # Trend Line (MA20)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend', line=dict(color='yellow', width=2)), row=1, col=1)
        
        # MACD
        fig.add_trace(go.Bar(x=df.index, y=df['Hist'], name='Momentum', marker_color=['green' if x >=0 else 'red' for x in df['Hist']]), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

draw_nifty_chart()

# --- 4. NIFTY 50 SPOT PRICE (FULL NUMBERS) ---
st.markdown("---")
df_n = yf.Ticker("^NSEI").history(period="1d", interval="1m")
if not df_n.empty:
    ltp = df_n['Close'].iloc[-1]
    hi, lo = df_n['High'].max(), df_n['Low'].min()
    
    st.markdown(f"""
        <div style='background:#1e1e1e; padding:30px; border-radius:20px; text-align:center; border:2px solid {pcr_color};'>
            <h3 style='color:gray; margin:0;'>NIFTY 50 SPOT PRICE</h3>
            <h1 style='color:white; font-size:80px; margin:10px 0;'>{ltp:,.2f}</h1>
            <div style='display:flex; justify-content:center; gap:50px;'>
                <h3 style='color:#00c853;'>BULLISH > {hi:,.2f}</h3>
                <h3 style='color:#ff1744;'>BEARISH < {lo:,.2f}</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
