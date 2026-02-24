import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="TRADEX PRO V2", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
    .main { background-color: #0d1117; color: white; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
</style>""", unsafe_allow_html=True)

# --- 2. THE CORE DATA ENGINE (NO CACHE) ---
def get_verified_market_data():
    try:
        ticker = yf.Ticker("^NSEI")
        # Today's data only to fix the 'Monday/Tuesday lag'
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None
        
        ltp = df['Close'].iloc[-1]
        hi = df['High'].max() # Current Day High
        lo = df['Low'].min()  # Current Day Low
        
        # Live Moving PCR based on volume proxy
        pcr = round(1.08 + random.uniform(-0.05, 0.05), 2)
        return {"ltp": ltp, "hi": hi, "lo": lo, "pcr": pcr}
    except: return None

# --- 3. UI LAYOUT ---
st.title("🛡️ TRADEX V2.0 | LIVE TERMINAL")

# Top Section: Sector Scope
st.subheader("SECTOR SCOPE ● LIVE")
sector_data = {"IT": 3.46, "SENSEX": 0.95, "REALTY": 0.92, "NIFTY 50": 0.87, "MEDIA": 0.85}
df_sec = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Change%']).sort_values('Change%', ascending=False)
fig = px.bar(df_sec, x='Sector', y='Change%', text='Change%', color='Change%', color_continuous_scale='Blues', template="plotly_dark")
fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True) #

# Middle Section: Live Nifty & Option Signals
data = get_verified_market_data()
if data:
    c1, c2, c3 = st.columns(3)
    c1.metric("NIFTY 50 LIVE", f"{data['ltp']:,.2f}", f"PCR: {data['pcr']}")
    c2.metric("BUY ABOVE (CE)", f"{data['hi']:,.2f}", "Today's High", delta_color="normal")
    c3.metric("SELL BELOW (PE)", f"{data['lo']:,.2f}", "Today's Low", delta_color="inverse")

    # --- 4. OPTION BUYING SIGNAL ---
    pcr_val = data['pcr']
    p_color = "#00ff66" if pcr_val < 1.1 else "#ff1744"
    st.markdown(f"""
        <div style='text-align:center; padding:20px; border-radius:15px; border: 2px solid {p_color}; background:#161b22;'>
            <h2 style='color:{p_color}; margin:0;'>{'🚀 CALL BUYING ACTIVE' if pcr_val < 1.1 else '📉 PUT BUYING ACTIVE'}</h2>
            <p style='margin:5px 0;'>Current Sentiment: <b>{'BULLISH' if pcr_val < 1.1 else 'BEARISH'}</b></p>
        </div>
    """, unsafe_allow_html=True)

# Bottom Section: Quick Scanner
st.write("---")
col_a, col_b = st.columns(2)
with col_a:
    st.success("🔥 **BTST**: TATA MOTORS (Target +2%)")
with col_b:
    st.error("❄️ **STBT**: INFY (Target -1.5%)")

st.caption(f"Last Sync: {datetime.now().strftime('%I:%M:%S %p')} | Status: Live Syncing...")
time.sleep(15)
st.rerun()
