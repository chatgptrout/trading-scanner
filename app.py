import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH ALL-IN-ONE", layout="wide")

# Dark Theme + Custom Boxes Styling (Screenshot 1000104752 Style)
st.markdown("""<style>
    .stApp { background-color: #010b14; color: white; }
    .signal-box { background: #0d1b2a; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b2b; height: 120px; }
    .price-text { font-size: 14px; color: #888; }
    .level-text { font-size: 18px; font-weight: bold; margin: 5px 0; }
</style>""", unsafe_allow_html=True)

# 1. DATA FETCHING
watchlist = ["SUNPHARMA.NS", "SBIN.NS", "DRREDDY.NS", "CIPLA.NS", "RELIANCE.NS", "CL=F"]

def get_data():
    rows = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            rows.append({"Symbol": s.replace(".NS",""), "Full": s, "Price": t['last_price'], 
                         "Change": ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100})
        except: continue
    return pd.DataFrame(rows)

df = get_data()

# 2. TOP SECTION: HEATMAP & CHART (Side-by-Side)
col_map, col_chart = st.columns([1, 2])

with col_map:
    st.markdown("### 🟥 DEEP RED HEATMAP")
    fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                     color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                     custom_data=['Full'])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=350, template="plotly_dark")
    selected = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_map")

with col_chart:
    active = "SUNPHARMA.NS"
    if selected and "selection" in selected and selected["selection"]["points"]:
        active = selected["selection"]["points"][0]["customdata"][0]
    
    st.markdown(f"### 📈 LIVE CHART: {active}")
    h = yf.Ticker(active).history(period='1d', interval='5m')
    chart = go.Figure(data=[go.Candlestick(x=h.index, open=h['Open'], high=h['High'], low=h['Low'], close=h['Close'],
                                         increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b')])
    chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(chart, use_container_width=True, key=f"chart_{active}")

# 3. BOTTOM SECTION: TRADEX SIGNALS (Exactly like 1000104752.jpg)
st.markdown("---")
st.markdown("### 🎯 TRADEX SIGNALS (QUICK MONEY)")
t1, t2, t3 = st.columns(3)

# Logic for dynamic levels
for (name, col, sym) in zip(["CRUDE OIL", "NIFTY", "BANK NIFTY"], [t1, t2, t3], ["CL=F", "^NSEI", "^NSEBANK"]):
    curr_p = yf.Ticker(sym).fast_info['last_price']
    
    if "CRUDE" in name:
        sig, color = f"BEARISH BELOW {int(curr_p*90 - 15)}", "#ff4b2b"
    else:
        sig, color = f"REVERSAL AT {int(curr_p + 45)}", "#00ff88"

    col.markdown(f"""<div class="signal-box">
        <h4 style="margin:0;">{name}</h4>
        <p class="level-text" style="color:{color};">{sig}</p>
        <p class="price-text">LTP: {curr_p:.2f}</p>
    </div>""", unsafe_allow_html=True)

time.sleep(20)
st.rerun()
