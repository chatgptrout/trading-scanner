import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="TRADEX PRO V63 - SIGNALS", layout="wide")

# Custom CSS (V63 Style)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .signal-buy { color: #00d084; font-weight: bold; background: rgba(0,208,132,0.1); padding: 5px; border-radius: 5px; }
    .signal-sell { color: #ff5252; font-weight: bold; background: rgba(255,82,82,0.1); padding: 5px; border-radius: 5px; }
    .card { background: #1c1f26; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATA ENGINE (YFINANCE) ---
def fetch_data():
    symbols = {
        "CRUDE OIL": "CL=F",
        "NATURAL GAS": "NG=F",
        "GOLD": "GC=F",
        "SILVER": "SI=F"
    }
    rows = []
    for name, sym in symbols.items():
        ticker = yf.Ticker(sym)
        # Fetching 5 days of data for EMA calculation
        df = ticker.history(period="5d", interval="1h")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            # EMA 9 Calculation
            ema9 = round(df['Close'].ewm(span=9, adjust=False).mean().iloc[-1], 2)
            
            # SIGNAL LOGIC
            if ltp > ema9:
                signal = "BUY 🟢"
            elif ltp < ema9:
                signal = "SELL 🔴"
            else:
                signal = "WAIT 🟡"
                
            rows.append({
                "COMMODITY": name,
                "LTP ($)": ltp,
                "EMA 9": ema9,
                "SIGNAL": signal
            })
    return pd.DataFrame(rows)

# --- 2. UI DASHBOARD ---
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"### 🦅 TRADEX PRO V63 | {datetime.now(IST).strftime('%H:%M:%S')}")

data = fetch_data()

# Main Display Table
st.table(data)

# --- 3. KEY LEVELS (PURANA FEATURES) ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.info("💡 **Trading Tip:** Always check EMA crossover before entry.")
with c2:
    st.warning("⚠️ **Alert:** Signals are based on 1H timeframe for stability.")

time.sleep(10)
st.rerun()
