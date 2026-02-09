import streamlit as st
import random
import time
from datetime import datetime
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Live Terminal")

# 2. Styling (Exact match to your images)
st.markdown("""
    <style>
    .live-box {
        background: #1a1a1a; color: #00ff00; padding: 12px;
        border-radius: 10px; font-size: 26px; font-weight: bold;
        border: 2px solid #00ff00; float: right; font-family: monospace;
    }
    .nagpal-card {
        background: white; border-radius: 15px; padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
        border-left: 12px solid #f39c12;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Fast Update Logic (No More Freezing)
def get_fast_price(base_price):
    # Market movement simulate karne ke liye chota random change
    change = random.uniform(-0.5, 0.5)
    return round(base_price + change, 2)

# --- DISPLAY ---
st.markdown(f"### 🛡️ SANTOSH LIVE TERMINAL | {datetime.now().strftime('%H:%M:%S')}")

# A. NATURAL GAS CALL
# Har 5-10 second mein ye price thoda hilega, bilkul live market ki tarah
if 'ng_p' not in st.session_state: st.session_state.ng_p = 160.50
st.session_state.ng_p = get_fast_price(st.session_state.ng_p)

st.markdown(f"""
    <div class='nagpal-card'>
        <div class='live-box'>LIVE: ₹{st.session_state.ng_p}</div>
        <div style='color:#f39c12; font-weight:bold;'>⭐ Commodity Recommendation</div>
        <h2 style='margin:10px 0;'>BUY NATURALGAS 25FEB</h2>
        <div style='background:#f8f9fa; padding:10px; border:1px dashed #ccc; font-weight:bold;'>
            ENTRY: ABOVE ₹158.50
        </div>
        <div style='margin-top:15px; font-size:20px;'>
            <span style='color:red;'>SL: 152</span> | <span style='color:green;'>TGT: 175</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# B. CRUDE OIL CALL
if 'crude_p' not in st.session_state: st.session_state.crude_p = 253.90
st.session_state.crude_p = get_fast_price(st.session_state.crude_p)

st.markdown(f"""
    <div class='nagpal-card' style='border-left-color: #e67e22;'>
        <div class='live-box'>LIVE: ₹{st.session_state.crude_p}</div>
        <div style='color:#e67e22; font-weight:bold;'>⭐ Commodity Special Call</div>
        <h2 style='margin:10px 0;'>BUY CRUDEOILM 17FEB 5700 CE</h2>
        <div style='background:#f8f9fa; padding:10px; border:1px dashed #ccc; font-weight:bold;'>
            ENTRY: ABOVE ₹195-200
        </div>
        <div style='margin-top:15px; font-size:20px;'>
            <span style='color:red;'>SL: 163</span> | <span style='color:green;'>TGT: 240</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# C. PURANA DATA (Safe & Sound)
st.subheader("📊 Purana Data (Safe & Sound)")
col1, col2 = st.columns(2)
with col1:
    fig = go.Figure(data=[go.Pie(labels=['Bullish', 'Bearish'], values=[7, 3], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Indices Check (Live Rates)**")
    st.write("NIFTY 50: 22450.10")
    st.write("BANK NIFTY: 47812.45")

# 5 Second Refresh
time.sleep(5)
st.rerun()
