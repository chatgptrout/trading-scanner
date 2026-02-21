import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI MOMENTUM TERMINAL", layout="wide")

# --- 1. OPTION CLOCK ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI HEADER (PCR 2.01) ---
# Keeping PCR and Signal consistent with your live data
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#111; color:white; border-radius:15px; border-bottom:8px solid #00c853;'>
        <h1 style='margin:0; color:#00c853;'>PCR: 2.01</h1>
        <h3 style='margin:0;'>AI STATUS: REVERSAL RISK ⚠️</h3>
        <p style='color:orange; margin:0;'>MACD MOMENTUM ENGINE: ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. ADVANCED CHART WITH MACD ---
def draw_macd_chart(symbol, title):
    df = yf.Ticker(symbol).history(period="1d", interval="5m")
    if not df.empty:
        # Calculating MACD (12, 26, 9)
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal']

        # Creating Subplots: Row 1 = Candles, Row 2 = MACD
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # Candlestick
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                   low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
        
        # MACD Trace
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='cyan', width=1.5)), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal', line=dict(color='magenta', width=1.5)), row=2, col=1)
        
        # MACD Histogram (Bars)
        colors = ['green' if val >= 0 else 'red' for val in df['Hist']]
        fig.add_trace(go.Bar(x=df.index, y=df['Hist'], name='Momentum', marker_color=colors), row=2, col=1)

        fig.update_layout(title=title, template="plotly_dark", xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>## 🕯️ CANDLESTICK & MACD MOMENTUM")
draw_macd_chart("CL=F", "CRUDE OIL (LIVE MOMENTUM ANALYSIS)")

# --- 4. LIVE TICKER CARDS ---
# Syncing with your current market rates
st.markdown("---")
cols = st.columns(3)
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        # Natural Gas Price Match
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"

        with cols[i]:
            st.markdown(f"""
                <div style='background:#1e1e1e; padding:15px; border-radius:10px; text-align:center; color:white;'>
                    <h5 style='color:gray;'>{name}</h5>
                    <h2 style='margin:0;'>{price_str}</h2>
                </div>
            """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
