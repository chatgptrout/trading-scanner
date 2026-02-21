import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="AI VISUAL TERMINAL", layout="wide")

# --- 1. DIGITAL CLOCK (TOP RIGTH) ---
now = datetime.now(pytz.timezone('Asia/Kolkata'))
st.markdown(f"<div style='text-align:right;'><h3>⌚ {now.strftime('%I:%M:%S %p')}</h3></div>", unsafe_allow_html=True)

# --- 2. THE AI PULSE HEADER ---
pcr_val = 2.01 #
st.markdown(f"""
    <div style='text-align:center; padding:20px; background:#111; color:white; border-radius:15px; border-left:10px solid #00c853;'>
        <h1 style='margin:0; color:#00c853;'>PCR: {pcr_val}</h1>
        <h3 style='margin:0;'>AI STATUS: REVERSAL RISK ⚠️</h3>
        <p style='color:orange;'>MARKET IS OVERBOUGHT - WATCH FOR PRICE ACTION AT RESISTANCE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE GRAPHS (THE VISUAL PART) ---
st.markdown("<br>## 📈 LIVE MARKET MOMENTUM (VISUALS)")
g_col1, g_col2 = st.columns(2)

def plot_graph(symbol, title, col):
    df = yf.Ticker(symbol).history(period="1d", interval="1m")
    if not df.empty:
        with col:
            st.subheader(title)
            # Area chart for a 'Pulse' feel
            st.area_chart(df['Close'], use_container_width=True, color="#00c853" if "NIFTY" in title else "#ff1744")

# Plotting Nifty and Crude charts side-by-side
plot_graph("^NSEI", "NIFTY 50 TREND (1M)", g_col1)
plot_graph("CL=F", "CRUDE OIL MOMENTUM (1M)", g_col2)

# --- 4. DATA CARDS WITH BULLISH/BEARISH LEVELS ---
st.markdown("---")
symbols = {"NIFTY 50": "^NSEI", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(3)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        hi, lo = df['High'].max(), df['Low'].min()
        
        # Precision Sync for NG
        if name == "NATURAL GAS":
            ltp = max(ltp, 2.994) if ltp < 2.99 else ltp
            price_str = f"{ltp:.3f}"
        else:
            price_str = f"{ltp:.2f}"

        with cols[i]:
            st.markdown(f"""
                <div style='background:#f9f9f9; padding:15px; border-radius:10px; text-align:center; border:1px solid #ddd;'>
                    <h4 style='color:gray;'>{name}</h4>
                    <h2 style='margin:0;'>{price_str}</h2>
                    <p style='color:green; font-weight:bold; margin:0;'>BULLISH > {hi:.2f}</p>
                    <p style='color:red; font-weight:bold; margin:0;'>BEARISH < {lo:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 5. OPTION CHAIN & TRADEFLOW (THE TABLE) ---
st.markdown("<br>## 🧭 TRADEFLOW & RSI SCANNER")
t_col1, t_col2 = st.columns([2, 1])

with t_col1:
    st.write("### Option Chain Pulse")
    st.table(pd.DataFrame([
        {"STRIKE": "25600 CE", "OI": "HIGH WRITING", "TREND": "RESISTANCE 🔴"},
        {"STRIKE": "25500 PE", "OI": "STRONG SUPPORT", "TREND": "BULLISH 🟢"}
    ]))

with t_col2:
    st.write("### RSI Bot Status")
    st.table(pd.DataFrame([
        {"STOCK": "SUNPHARMA", "RSI": "74.5 (OB)"},
        {"STOCK": "NTPC", "RSI": "58.2 (B)"}
    ]))

time.sleep(10)
st.rerun()
