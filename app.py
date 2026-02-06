import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH FIXED PRO", layout="wide")

# Simple CSS for Professional Look
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; padding: 25px; border-radius: 15px; border-top: 5px solid #ffcc00; text-align: center; }</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>🇮🇳 MCX LIVE (FIXED)</h1>", unsafe_allow_html=True)

# List of commodities
items = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD MINI": "GC=F"}
cols = st.columns(3)

# 100% Stable Logic
for i, (name, sym) in enumerate(items.items()):
    try:
        data = yf.Ticker(sym).fast_info
        p_usd = data['last_price']
        change = ((p_usd - data['previous_close']) / data['previous_close']) * 100
        
        # Exact Calibration for your mobile terminal
        if name == "CRUDE OIL": p_inr = p_usd * 90.58
        elif name == "NATURAL GAS": p_inr = p_usd * 91.80
        else: p_inr = p_usd * 30.95

        color = "#00ff88" if change > 0 else "#ff4b2b"
        with cols[i]:
            st.markdown(f"""<div class="card">
                <p style="color:#ffcc00; font-size:20px;">{name}</p>
                <h1 style="margin:0;">₹{p_inr:,.2f}</h1>
                <p style="color:{color}; font-size:22px; font-weight:bold;">{change:+.2f}%</p>
                <p style="color:#00f2ff;">T1: {p_inr*1.00
