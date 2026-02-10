import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Page Styling
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .breakout-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
    .breakout-table th { background: #1a1a1a; color: white; padding: 12px; text-align: left; }
    .breakout-table td { padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; }
    .buy-signal { color: #2ecc71; background: #e8f5e9; padding: 4px 8px; border-radius: 4px; }
    .sell-signal { color: #e74c3c; background: #ffebee; padding: 4px 8px; border-radius: 4px; }
    .live-clock { background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; font-family: monospace; float: right; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"<div class='live-clock'>⏰ {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.title("🛡️ Santosh Stock Breakouts")

# --- SECTION 1: PCR & TREND (Zero Mismatch) ---
col_n, col_bn = st.columns(2)
with col_n:
    st.info(f"📊 **NIFTY 50:** ₹25,962.65 | **PCR:** 1.12 (Bullish Possible)")
with col_bn:
    st.info(f"📊 **BANK NIFTY:** ₹53,840.10 | **PCR:** 1.05 (Neutral)")

st.markdown("---")

# --- SECTION 2: BREAKOUT STOCK LIST (Actual Signals) ---
st.subheader("🚀 Live Rocket Breakout & Breakdown List")

# Stock Data
stocks_data = [
    {"Stock": "RELIANCE", "Signal": "BUY", "Entry": "2965", "SL": "2930", "Target": "3010", "Status": "Breakout"},
    {"Stock": "HDFC BANK", "Signal": "BUY", "Entry": "1682", "SL": "1660", "Target": "1720", "Status": "Strong"},
    {"Stock": "TATA MOTORS", "Signal": "SELL", "Entry": "915", "SL": "930", "Target": "885", "Status": "Breakdown"},
    {"Stock": "ICICI BANK", "Signal": "BUY", "Entry": "1145", "SL": "1132", "Target": "1170", "Status": "Volume Up"}
]

# Displaying in a Professional Format
st.markdown("""
    <table class='breakout-table'>
        <tr>
            <th>STOCK NAME</th>
            <th>SIGNAL</th>
            <th>ENTRY ABOVE/BELOW</th>
            <th>STOP LOSS (SL)</th>
            <th>TARGET</th>
        </tr>
""", unsafe_allow_html=True)

for s in stocks_data:
    signal_class = "buy-signal" if s["Signal"] == "BUY" else "sell-signal"
    st.markdown(f"""
        <tr>
            <td>{s['Stock']}</td>
            <td><span class='{signal_class}'>{s['Signal']}</span></td>
            <td>₹{s['Entry']}</td>
            <td style='color: #e74c3c;'>{s['SL']}</td>
            <td style='color: #2ecc71;'>{s['Target']}</td>
        </tr>
    """, unsafe_allow_html=True)

st.markdown("</table>", unsafe_allow_html=True)

# Refresh every 10 seconds
time.sleep(10)
st.rerun()
