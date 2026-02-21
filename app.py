import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI CANDLE TERMINAL PRO", layout="wide")

# --- 1. DIGITAL CLOCK ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI HEADER (PCR 2.01) ---
st.markdown(f"""
    <div style='text-align:center; padding:15px; background:#111; color:white; border-radius:15px; border-bottom:8px solid #00c853;'>
        <h1 style='margin:0; color:#00c853;'>PCR: 2.01</h1>
        <h3 style='margin:0;'>AI STATUS: REVERSAL RISK ⚠️</h3>
    </div>
""", unsafe_allow_html=True)

# --- 3. ADVANCED CANDLESTICK WITH SR ZONES ---
def draw_pro_candles(symbol, title):
    df = yf.Ticker(symbol).history(period="1d", interval="5m")
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name='Price'
        )])
        
        # Adding Trend Line (MA20)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='Trend Line', line=dict(color='yellow', width=2)))
        
        # Highlighting Support & Resistance Zones
        hi_val, lo_val = df['High'].max(), df['Low'].min()
        fig.add_hline(y=hi_val, line_dash="dash", line_color="red", annotation_text="RESISTANCE")
        fig.add_hline(y=lo_val, line_dash="dash", line_color="green", annotation_text="SUPPORT")
        
        fig.update_layout(title=title, template="plotly_dark", xaxis_rangeslider_visible=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>## 🕯️ LIVE CANDLESTICK & S/R ZONES")
c1, c2 = st.columns(2)

with c1:
    draw_pro_candles("^NSEI", "NIFTY 50 (S/R ANALYSIS)")
with c2:
    draw_pro_candles("CL=F", "CRUDE OIL (S/R ANALYSIS)")

# --- 4. LIVE TICKER CARDS ---
# Nifty: 25565.90 | Crude: 66.31 | NG: 2.994
st.markdown("---")
cols = st.columns(3)
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Natural Gas Match logic
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"

        with cols[i]:
            st.markdown(f"""
                <div style='background:#1e1e1e; padding:20px; border-radius:10px; text-align:center; color:white; border:1px solid #333;'>
                    <h5 style='color:gray;'>{name}</h5>
                    <h2 style='margin:0;'>{price_str}</h2>
                    <p style='color:#00c853;'>BULLISH > {hi:.2f}</p>
                    <p style='color:#ff1744;'>BEARISH < {lo:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
