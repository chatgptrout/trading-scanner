import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH TRADEX ONLY", layout="wide")

# Dark Theme + Tradex Box Styling
st.markdown("""<style>
    .stApp { background-color: #010b14; color: white; }
    .tradex-card { 
        background: #0d1b2a; padding: 25px; border-radius: 12px; 
        border-left: 8px solid #ff4b2b; margin-bottom: 20px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .level-val { font-size: 24px; font-weight: bold; color: #ff4b2b; margin-top: 10px; }
    .ltp-val { font-size: 14px; color: #888; }
</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#1a73e8;'>🎯 TRADEX LIVE SIGNALS</h1>", unsafe_allow_html=True)

# 1. HEATMAP SECTION (As per your 1000104630.jpg preference)
import plotly.express as px
watchlist = ["SUNPHARMA.NS", "SBIN.NS", "DRREDDY.NS", "CIPLA.NS", "RELIANCE.NS", "CL=F"]

def get_map_data():
    rows = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            rows.append({"Symbol": s.replace(".NS",""), "Price": t['last_price'], 
                         "Change": ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100})
        except: continue
    return pd.DataFrame(rows)

df = get_map_data()
st.markdown("### 🟥 MARKET HEATMAP")
fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# 2. TRADEX SIGNALS SECTION (The main thing you wanted)
st.markdown("---")
st.markdown("### 🚀 QUICK MONEY LEVELS")
c1, c2, c3 = st.columns(3)

scripts = [("CRUDE OIL", "CL=F"), ("NIFTY", "^NSEI"), ("BANK NIFTY", "^NSEBANK")]
cols = [c1, c2, c3]

for (name, sym), col in zip(scripts, cols):
    try:
        curr_p = yf.Ticker(sym).fast_info['last_price']
        if "CRUDE" in name:
            signal = f"BEARISH BELOW {int(curr_p*90.5 - 15)}"
            color = "#ff4b2b"
        else:
            signal = f"REVERSAL AT {int(curr_p + 50)}"
            color = "#00ff88"
            
        col.markdown(f"""<div class="tradex-card">
            <h3 style="margin:0;">{name}</h3>
            <div class="level-val" style="color:{color};">{signal}</div>
            <div class="ltp-val">LTP: {curr_p:.2f}</div>
        </div>""", unsafe_allow_html=True)
    except: continue

time.sleep(30)
st.rerun()
