import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. UI Styling (Telegram Message Style)
st.markdown("""
    <style>
    .trade-alert-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        border-left: 8px solid #2ecc71;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #333;
    }
    .trade-alert-sell { border-left-color: #e74c3c; }
    .label-blue { color: #1976d2; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Trade Calculator Logic (Entry, SL, Targets)
def generate_trade_details(symbol, current_price, signal_type):
    if signal_type == "BUY":
        sl = round(current_price * 0.985, 2) # 1.5% SL
        t1 = round(current_price * 1.02, 2)  # 2% Target
        t2 = round(current_price * 1.05, 2)  # 5% Target
        return {"action": "BUY", "cmp": current_price, "sl": sl, "targets": f"{t1} - {t2}", "color": "trade-alert-card"}
    else:
        sl = round(current_price * 1.015, 2)
        t1 = round(current_price * 0.98, 2)
        return {"action": "SELL", "cmp": current_price, "sl": sl, "targets": f"{t1}", "color": "trade-alert-card trade-alert-sell"}

# 3. Main Display
st.title("🔥 Santosh Live Trade Signals")

# Simulated Signal (Jaise hi breakout hoga, ye card dikhega)
trade = generate_trade_details("LTF", 295.0, "BUY") #

st.markdown(f"""
    <div class='{trade['color']}'>
        <h3 style='margin-top:0;'>🚀 Trade Alert: {trade['action']} LTF</h3>
        <p><b>CMP:</b> {trade['cmp']}</p>
        <p><b>SL:</b> <span style='color:#e74c3c;'>{trade['sl']}</span></p>
        <p><b>Target:</b> <span style='color:#2ecc71;'>{trade['targets']}</span></p>
        <hr>
        <p style='font-size:12px; color:#888;'>Disclaimer: Trade after reading rules.</p>
    </div>
    """, unsafe_allow_html=True)
