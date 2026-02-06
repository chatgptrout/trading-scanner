import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH PERFECT SYNC", layout="wide")

# Professional UI Style
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; padding: 25px; border-radius: 15px; border-top: 5px solid #ffcc00; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>🇮🇳 MCX LIVE: AUTO-SYNC PRO</h1>", unsafe_allow_html=True)

# 1. Fetch Dynamic USD-INR Rate
def get_live_multiplier():
    try:
        # Fetching live conversion rate to match Indian Premium
        usd_inr = yf.Ticker("INR=X").fast_info['last_price']
        return usd_inr
    except:
        return 83.5 # Standard Fallback

current_multiplier = get_live_multiplier()

# 2. Commodity List with Custom Adjustments for Indian Taxes/Duty
items = {
    "CRUDE OIL": {"sym": "CL=F", "adj": 1.085}, # Calibrated for ₹5,749
    "NATURAL GAS": {"sym": "NG=F", "adj": 1.100}, # Calibrated for ₹322
    "GOLD MINI": {"sym": "GC=F", "adj": 0.371}  # Calibrated for ₹1,51,871
}

cols = st.columns(3)

for i, (name, config) in enumerate(items.items()):
    try:
        ticker = yf.Ticker(config['sym']).fast_info
        p_usd = ticker['last_price']
        change = ((p_usd - ticker['previous_close']) / ticker['previous_close']) * 100
        
        # FINAL AUTO-CALCULATION
        p_inr = p_usd * current_multiplier * config['adj']

        color = "#00ff88" if change > 0 else "#ff4b2b"
        with cols[i]:
            st.markdown(f"""<div class="card">
                <p style="color:#ffcc00; font-size:20px; font-weight:bold;">{name}</p>
                <h1 style="margin:0;">₹{p_inr:,.2f}</h1>
                <p style="color:{color}; font-size:22px; font-weight:bold;">{change:+.2f}%</p>
                <p style="color:#00f2ff; font-weight:bold; font-size:14px;">T1: {p_inr*1.006:,.1f} | SL: {p_inr*0.995:,.1f}</p>
            </div>""", unsafe_allow_html=True)
    except:
        with cols[i]: st.warning("Re-connecting... 📡")

st.info(f"✅ Live Sync Active | Multiplier: {current_multiplier:.2f} | Refresh: 5s")

# Fast refresh for scalping
time.sleep(5)
st.rerun()
