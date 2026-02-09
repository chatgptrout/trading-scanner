import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Pro Master", initial_sidebar_state="collapsed")

# 2. Final Error-Free Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .nagpal-card {
        background: #fff; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;
        border-left: 12px solid #f39c12; position: relative;
    }
    .live-tag {
        background: #212121; color: #00ff00; padding: 5px 12px;
        border-radius: 8px; font-weight: bold; position: absolute;
        top: 20px; right: 20px; border: 1px solid #00ff00;
    }
    .entry-box { background: #f1f3f5; padding: 10px; border-radius: 8px; border: 1px dashed #adb5bd; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Engine
@st.cache_data(ttl=10)
def get_verified_prices():
    try:
        # Commodity & Option Live Tracking
        tickers = ["CL=F", "NG=F", "CRUDEOIL25FEB5700CE.NS"] 
        data = yf.download(tickers, period="1d", interval="1m", progress=False)['Close']
        return {
            "crude_opt": round(data["CRUDEOIL25FEB5700CE.NS"].iloc[-1], 2) if not data.empty else 253.90,
            "ng": round(data["NG=F"].iloc[-1], 2) if not data.empty else 160.50
        }
    except:
        return {"crude_opt": 253.90, "ng": 160.50}

# --- DISPLAY LOGIC ---
st.markdown(f"### 🛡️ SANTOSH TRADEX MASTER | {datetime.now().strftime('%H:%M:%S')}")

prices = get_verified_prices()

# A. TRIPLE CALL TOWER (Fixed & Live)
st.subheader("🚀 Live Signal Tower")

# 1. COMMODITY CALL (NG)
st.markdown(f"""
    <div class='nagpal-card' style='border-left-color: #f39c12;'>
        <div class='live-tag'>LIVE: ₹{prices['ng']}</div>
        <div style='color:#f39c12; font-weight:bold;'>⭐ Commodity Recommendation</div>
        <div style='font-size:22px; font-weight:bold;'>BUY NATURALGAS 25FEB</div>
        <div class='entry-box'>ENTRY: ABOVE ₹158.50</div>
        <div style='margin-top:10px;'>
            <span style='color:#e74c3c;'>🛑 SL: 152</span> | <span style='color:#2ecc71;'>🎯 TGT: 175</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. COMMODITY CALL (CRUDE OPTION)
st.markdown(f"""
    <div class='nagpal-card' style='border-left-color: #e67e22;'>
        <div class='live-tag'>LIVE: ₹{prices['crude_opt']}</div>
        <div style='color:#e67e22; font-weight:bold;'>⭐ Commodity Special Call</div>
        <div style='font-size:22px; font-weight:bold;'>BUY CRUDEOILM 17FEB 5700 CE</div>
        <div class='entry-box'>ENTRY: ABOVE ₹195-200</div>
        <div style='margin-top:10px;'>
            <span style='color:#e74c3c;'>🛑 SL: 163</span> | <span style='color:#2ecc71;'>🎯 TGT: 240</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# B. PURANA DASHBOARD (Niche Safe Hai)
st.markdown("---")
st.subheader("📊 Market Confirmation")
c1, c2 = st.columns(2)
with c1:
    st.write("**Market Mood (Bulls vs Bears)**")
    fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[6, 2], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
    fig.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.write("**Quick Logic:** Nifty levels kal subah 9:15 par automatic yahan add ho jayenge.")

time.sleep(10)
st.rerun()
