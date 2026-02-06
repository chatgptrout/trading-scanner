import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH MASTER CONTROL", layout="wide")

st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.mcx-card { background: #0d1b2a; padding: 20px; border-radius: 15px; border-top: 5px solid #ffcc00; margin-bottom: 20px; text-align: center; }
.price-big { font-size: 45px; font-weight: bold; color: #ffffff; }</style>""", unsafe_allow_html=True)

# --- NEW: MANUAL CALIBRATION CONTROLS ---
st.sidebar.header("⚙️ RATE CALIBRATION")
st.sidebar.info("Adjust these to match your mobile app exactly")
crude_adj = st.sidebar.slider("Crude Oil Adjustment", 85.0, 95.0, 90.65, 0.05)
gold_adj = st.sidebar.slider("Gold Adjustment", 30.0, 35.0, 30.98, 0.01)
ng_adj = st.sidebar.slider("NG Adjustment", 85.0, 95.0, 91.85, 0.05)

st.markdown("<h1 style='text-align:center; color:#ffcc00;'>🇮🇳 MCX LIVE: MASTER CONTROL</h1>", unsafe_allow_html=True)

mcx_data = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F", "GOLD MINI": "GC=F"}
cols = st.columns(3)

for (name, sym), col in zip(mcx_data.items(), cols):
    try:
        t = yf.Ticker(sym)
        p_usd = t.fast_info['last_price']
        change = ((p_usd - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # APPLYING YOUR MANUAL ADJUSTMENT
        if name == "CRUDE OIL": p_inr = p_usd * crude_adj
        elif name == "NATURAL GAS": p_inr = p_usd * ng_adj
        else: p_inr = p_usd * gold_adj

        color = "#00ff88" if change > 0 else "#ff4b2b"
        with col:
            st.markdown(f"""
                <div class="mcx-card">
                    <p style="color:#ffcc00; font-size:20px;">{name}</p>
                    <p class="price-big">₹{p_inr:,.2f}</p>
                    <p style="color:{color}; font-size:24px; font-weight:bold;">{change:+.2f}%</p>
                    <p style="color:#00f2ff;">T1: {p_inr*1.006:,.1f} | SL: {p_inr*0.995:,.1f}</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(5)
st.rerun()
