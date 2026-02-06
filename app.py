import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH PERFECT MATCH", layout="wide")

# Sidebar for Manual Calibration (To fix the 6212 vs 5713 gap)
st.sidebar.header("⚙️ RATE CALIBRATION")
st.sidebar.info("App par ₹5,713 hai? Slider ko peeche kijiye.")
# Manual Multiplier adjustment
multiplier_fix = st.sidebar.slider("Crude Adjustment", 80.0, 95.0, 89.92, 0.05)

st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; padding: 25px; border-radius: 15px; border-top: 5px solid #ffcc00; text-align: center; }</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>🇮🇳 MCX LIVE: ZERO ERROR</h1>", unsafe_allow_html=True)

items = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
cols = st.columns(2)

for i, (name, sym) in enumerate(items.items()):
    try:
        t = yf.Ticker(sym).fast_info
        p_usd = t['last_price']
        change = ((p_usd - t['previous_close']) / t['previous_close']) * 100
        
        # Using the Sidebar Multiplier to force a match
        if name == "CRUDE OIL":
            p_inr = p_usd * multiplier_fix 
        else:
            p_inr = p_usd * (multiplier_fix + 1.2) # NG adjustment

        color = "#00ff88" if change > 0 else "#ff4b2b"
        with cols[i]:
            st.markdown(f"""<div class="card">
                <p style="color:#ffcc00; font-size:20px;">{name}</p>
                <h1 style="margin:0;">₹{p_inr:,.2f}</h1>
                <p style="color:{color}; font-size:22px; font-weight:bold;">{change:+.2f}%</p>
            </div>""", unsafe_allow_html=True)
    except Exception:
        st.error("📡 Syncing...")

time.sleep(5)
st.rerun()
