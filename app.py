import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH AUTO-MCX", layout="wide")

# Premium UI
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.mcx-card { background: #0d1b2a; padding: 25px; border-radius: 15px; border-top: 5px solid #ffcc00; margin-bottom: 20px; text-align: center; }
.price-big { font-size: 44px; font-weight: bold; color: #ffffff; }</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>🚀 AUTO-MATCH MCX LIVE</h1>", unsafe_allow_html=True)

# Assets mapping
mcx_data = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD MINI": "GC=F"}

# Automatic INR Multiplier Logic (Dynamic)
def get_auto_multiplier():
    try:
        # Live USD-INR rate fetch
        usd_inr = yf.Ticker("INR=X").fast_info['last_price']
        return usd_inr
    except:
        return 83.5 # Fallback

auto_inr = get_auto_multiplier()
cols = st.columns(3)

for (name, sym), col in zip(mcx_data.items(), cols):
    try:
        t = yf.Ticker(sym)
        p_usd = t.fast_info['last_price']
        change = ((p_usd - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # AUTO-CONVERSION MATH
        if name == "CRUDE OIL":
            # WTI to MCX Crude Conversion (Automatic)
            p_inr = p_usd * auto_inr * 1.
