import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH TRADEX MASTER", layout="wide")

# Dark Premium Theme (No Chart Focus)
st.markdown("""<style>
    .stApp { background-color: #010b14; color: white; }
    .signal-box { 
        background: #0d1b2a; padding: 15px; border-radius: 12px; 
        border-left: 6px solid #ff4b2b; height: 140px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .level-val { font-size: 20px; font-weight: bold; margin-top: 8px; }
    .ltp-val { font-size: 12px; color: #888; margin-top: 5px; }
</style>""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#1a73e8; margin-bottom:0;'>🎯 TRADEX LIVE SIGNALS</h2>", unsafe_allow_html=True)

# 1. COMPACT HEATMAP (Fixed Size for Better Look)
watchlist = ["RELIANCE.NS", "SBIN.NS", "DRREDDY.NS", "SUNPHARMA.NS", "CIPLA.NS", "CL=F"]

def get_data():
    rows = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            rows.append({"Symbol": s.replace(".NS",""), "Change": ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100})
        except: continue
    return pd.DataFrame(rows)

df = get_data()
if not df.empty:
    fig = px.treemap(df, path=['Symbol'], values=[1]*len(df), # Fixed size boxes for clean look
                     color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'])
    # Height kam kar di hai taaki signals upar aayein
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=250, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 2. QUICK MONEY LEVELS (Side-by-Side like 1000104752.jpg)
st.markdown("### 🚀 QUICK MONEY LEVELS")
c1, c2, c3 = st.columns(3)

scripts = [("CRUDE OIL", "CL=F"), ("NIFTY", "^NSEI"), ("BANK NIFTY", "^NSEBANK")]
for (name, sym), col in zip(scripts, [c1, c2, c3]):
    try:
        t = yf.Ticker(sym).fast_info
        curr_p = t['last_price']
        if "CRUDE" in name:
            signal, color = f"BEARISH BELOW {int(curr_p*90.5 - 15)}", "#ff4b2b"
        else:
            signal, color = f"REVERSAL AT {int(curr_p + 50)}", "#00ff88"
            
        col.markdown(f"""<div class="signal-box">
            <h4 style="margin:0;">{name}</h4>
            <div class="level-val" style="color:{color};">{signal}</div>
            <div class="ltp-val">LTP: {curr_p:.2f}</div>
        </div>""", unsafe_allow_html=True)
    except: continue

time.sleep(20)
st.rerun()
