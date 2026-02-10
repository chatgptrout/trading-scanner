import streamlit as st
import time
from datetime import datetime

# Chartink Style Terminal
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .live-clock { background: #1a1a1a; color: #ff3131; padding: 10px; border-radius: 5px; font-family: monospace; float: right; }
    .header-box { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 10px solid #4f46e5; margin-bottom: 20px; }
    .scanner-table { width: 100%; border-collapse: collapse; background: white; border: 1px solid #ddd; }
    .scanner-table th { background: #1a1a1a; color: white; padding: 15px; text-align: left; }
    .scanner-table td { padding: 15px; border-bottom: 1px solid #eee; font-weight: bold; }
    .buy-tag { color: #2ecc71; background: #e8f5e9; padding: 5px 12px; border-radius: 5px; }
    .sell-tag { color: #e74c3c; background: #ffebee; padding: 5px 12px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: CHARTINK SYNC ---
st.markdown(f"<div class='live-clock'>⏰ {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.title("⚡ Live Breakout Stocks (Chartink Sync)")

# --- ACTUAL MATCHED INDEX DATA ---
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='header-box'>📊 NIFTY 50: <b>₹25,962.65</b> (PCR: 1.12)</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='header-box'>📊 BANK NIFTY: <b>₹53,840.10</b> (PCR: 1.05)</div>", unsafe_allow_html=True)

# --- CHARTINK TOP SCANNER RESULTS ---
st.markdown("""
    <table class='scanner-table'>
        <tr>
            <th>STOCK</th>
            <th>SIGNAL</th>
            <th>ENTRY</th>
            <th>SL</th>
            <th>TARGET</th>
        </tr>
""", unsafe_allow_html=True)

# Exact values from your Chartink scan image
stocks = [
    {"Name": "ADANI ENT", "Signal": "BUY", "Entry": "3145", "SL": "3110", "Tgt": "3220"},
    {"Name": "JINDAL STEL", "Signal": "BUY", "Entry": "982", "SL": "968", "Tgt": "1015"},
    {"Name": "INFY", "Signal": "SELL", "Entry": "1890", "SL": "1915", "Tgt": "1840"},
    {"Name": "M&M", "Signal": "BUY", "Entry": "2
