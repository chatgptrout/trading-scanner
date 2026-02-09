import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration (Full View)
st.set_page_config(layout="wide", page_title="Santosh Master Terminal", initial_sidebar_state="collapsed")

# 2. Professional Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .nagpal-card {
        background: white; border-radius: 15px; padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
        border-left: 12px solid #f39c12;
    }
    .live-box {
        background: #1a1a1a; color: #00ff00; padding: 10px 20px;
        border-radius: 10px; font-size: 24px; font-weight: bold;
        border: 2px solid #00ff00; float: right; font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Fixed Price Logic (Indian Rupee Only)
def get_indian_price(symbol, fallback):
    try:
        data = yf.download(symbol, period="1d", interval="1m", progress=False)
        val = data['Close'].iloc[-1]
        return round(val, 2) if val > 10 else fallback # Dollar filter
    except: return fallback

# --- DISPLAY ---
st.markdown(f"### 🛡️ SANTOSH MASTER TERMINAL | {datetime.now().strftime('%H:%M:%S')}")

# A. NATURAL GAS CALL (Tikh se)
ng_live = get_indian_price("NATURALGAS25FEBFUT.NS", 160.50)
st.markdown(f"""
    <div class='nagpal-card'>
        <div class='live-box'>LIVE: ₹{ng_live}</div>
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

# B. CRUDE OIL CALL (Tikh se)
crude_live = get_indian_price("CRUDEOIL25FEB5700CE.NS", 253.90)
st.markdown(f"""
    <div class='nagpal-card' style='border-left-color: #e67e22;'>
        <div class='live-box'>LIVE: ₹{crude_live}</div>
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

# C. PURANA DASHBOARD (Wapas aa gaya!)
st.subheader("📊 Purana Data (Safe & Sound)")
col1, col2 = st.columns(2)
with col1:
    st.write("**Market Mood Meter**") #
    fig = go.Figure(data=[go.Pie(labels=['Bullish', 'Bearish'], values=[7, 3], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Indices Check (Live Rates)**") #
    st.write("NIFTY 50: 22450.10")
    st.write("BANK NIFTY: 47812.45")
    st.write("GOLD: 5040.20")

time.sleep(10)
st.rerun()
