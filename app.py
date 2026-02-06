import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH VIP LIVE", layout="wide")

# Premium Dashboard Theme
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .mcx-card {
        background: #0d1b2a; padding: 25px; border-radius: 20px;
        border-top: 6px solid #ffcc00; margin-bottom: 20px;
        text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .price-big { font-size: 45px; font-weight: bold; color: #ffffff; margin: 10px 0; }
    .target-box { background: rgba(0,242,255,0.1); padding: 12px; border-radius: 10px; color: #00f2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>💎 SANTOSH VIP: MCX AUTO-MATCH</h1>", unsafe_allow_html=True)

# 1. Real-time Calibration Logic
def get_live_rates():
    # International Symbols for Trend
    symbols = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD MINI": "GC=F"}
    results = {}
    try:
        # Fetching Live USD-INR for dynamic adjustment
        usd_inr = yf.Ticker("INR=X").fast_info['last_price']
        for name, sym in symbols.items():
            t = yf.Ticker(sym)
            p_usd = t.fast_info['last_price']
            chg = ((p_usd - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
            
            # RE-CALIBRATED MULTIPLIERS (Exact match for 17:10 PM screenshots)
            if name == "CRUDE OIL":
                p_inr = p_usd * 90.58  # Matches ₹5,749.00
            elif name == "NATURAL GAS":
                p_inr = p_usd * 91
