import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time

# --- APP CONFIG ---
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

# Professional Trading Theme
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f7f9; }}
    .stock-card {{ background: white; border-top: 5px solid #2ecc71; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }}
    .clock-box {{ background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; text-align: center; font-family: monospace; font-size: 22px; border: 1px solid #333; }}
    
    /* News Ticker Styling */
    .ticker-wrapper {{ background: #1e1e2f; color: #d4af37; padding: 10px 0; overflow: hidden; white-space: nowrap; border-radius: 5px; margin-top: 20px; }}
    .ticker-text {{ display: inline-block; padding-left: 100%; animation: ticker 30s linear infinite; font-weight: bold; font-size: 16px; }}
    @keyframes ticker {{ 0% {{ transform: translate(0, 0); }} 100% {{ transform: translate(-100%, 0); }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. HEADER & CLOCK (KEEPING IT) ---
h1, h2 = st.columns([3, 1])
with h1:
    st.title("🚀 SANTOSH ULTIMATE TRADER")
with h2:
    st.markdown(f"<div class='clock-box'>⏰ {curr_time}</div>", unsafe_allow_html=True)

# --- SECTION REMOVED (ALERT & P&L TRACKER REMOVED AS REQUESTED) ---

# --- 2. VIP WATCHLIST (STARTING DIRECTLY HERE) ---
st.write("### ⭐ VIP Watchlist")
v1, v2, v3, v4, v5 = st.columns(5)
with v1: st.markdown("<div class='stock-card'><b>BSE LTD</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 3185</div>", unsafe_allow_html=True)
with v2: st.markdown("<div class='stock-card'><b>JINDALSTEL</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 1199</div>", unsafe_allow_html=True)
with v3: st.markdown("<div class='stock-card'><b>ADANI ENT</b><br><span style='color:blue;'>WATCHING</span><br>LTP: 3158</div>", unsafe_allow_html=True)
with v4: st.markdown("<div class='stock-card'><b>M&M</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 2852</div>", unsafe_allow_html=True)
with v5: st.markdown("<div class='stock-card' style='border-top-color:#e74c3c;'><b>CRUDE OIL</b><br><span style='color:red;'>WELL SET BEAR</span><br>LTP: 5812</div>", unsafe_allow_html=True)

st.divider()

# --- 3. % STRENGTH & ADV/DEC CHARTS (PURANA) ---
col_l, col_r = st.columns([2, 1])
with col_l:
    st.subheader("🏗️ Sector Strength (% Change)")
    fig = go.Figure(go.Bar(x=[0.26, 1.11, 1.44, 0.45, -0.99], y=['NIFTY', 'BSE', 'JINDAL', 'M&M', 'CRUDE'], orientation='h', marker_color='#4f46e5'))
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("🔴 Market Health")
    fig_pie = go.Figure(data=[go.Pie(labels=['Advance', 'Decline'], values=[76, 24], hole=.6, marker_colors=['#2ecc71', '#e74c3c'])])
    fig_pie.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 4. COMMODITY & NEWS TICKER (PURANA) ---
st.divider()
st.subheader("💰 MCX Commodity Live Session")
mcx1, mcx2, mcx3 = st.columns(3)
mcx1.metric("CRUDE OIL", "₹5,812", "-0.99%")
mcx2.metric("NATURAL GAS", "₹279.30", "-2.85%")
mcx3.metric("GOLD", "₹72,450", "+0.12%")

st.markdown("""
    <div class='ticker-wrapper'>
        <div class='ticker-text'>
            🚀 BREAKOUT ALERT: BSE confirms trend above 3150... 🔥 CRUDE OIL trading near crucial support 5800... 📈 NIFTY target for tomorrow: 26050... 💡 Nagpal Strategy: Focus on PSU Banks in first 15 mins... ⚠️ Keep Stoploss tight on Adani Enterprise... 
        </div>
    </div>
    """, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
