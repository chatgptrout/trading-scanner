import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH PC PRO", layout="wide")

# Dark Glass UI Style
st.markdown("""<style>
    .stApp { background-color: #010b14; color: white; }
    .tradex-box { background: #0d1b2a; padding: 20px; border-radius: 12px; border-left: 6px solid #ff4b2b; margin-bottom: 10px; }
    .price-up { color: #00ff88; font-weight: bold; }
    .price-down { color: #ff4b2b; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# 1. DATA ENGINE (Pharma + Heavyweights)
watchlist = ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS", "CL=F"]

def get_master_data():
    rows = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            p, c = t['last_price'], ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100
            rows.append({"Symbol": s.replace(".NS",""), "Full": s, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(rows)

df = get_master_data()

# 2. PC LAYOUT (Side-by-Side)
col1, col2 = st.columns([1.2, 2])

with col1:
    st.markdown("### 🟥 DEEP RED HEATMAP")
    fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                     color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                     custom_data=['Full'])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=400, template="plotly_dark")
    # Click interaction for PC
    selected = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="pc_heat")

with col2:
    # Sync Logic: Clicked stock ya default SUNPHARMA
    active = "SUNPHARMA.NS"
    if selected and "selection" in selected and selected["selection"]["points"]:
        active = selected["selection"]["points"][0]["customdata"][0]
    
    st.markdown(f"### 📈 LIVE CHART: {active}")
    h = yf.Ticker(active).history(period='1d', interval='5m')
    chart = go.Figure(data=[go.Candlestick(x=h.index, open=h['Open'], high=h['High'], low=h['Low'], close=h['Close'],
                                         increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b')])
    chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(chart, use_container_width=True, key=f"pc_chart_{active}")

# 3. TRADEX LEVELS (Bottom Section) - 1000104659.jpg Style
st.markdown("---")
st.markdown("### 🎯 TRADEX SIGNALS (QUICK MONEY)")
t1, t2, t3 = st.columns(3)

for (name, col) in zip(["CRUDE OIL", "NIFTY", "BANK NIFTY"], [t1, t2, t3]):
    # Example logic for levels based on current price
    sym = "CL=F" if "CRUDE" in name else ("^NSEI" if "NIFTY" == name else "^NSEBANK")
    curr_p = yf.Ticker(sym).fast_info['last_price']
    
    if "CRUDE" in name:
        level_p = int(curr_p * 90.5) # Crude Feb Fut estimation
        sig = f"BEARISH BELOW {level_p - 20}"
        color = "price-down"
    else:
        sig = f"REVERSAL AT {int(curr_p + 40)}"
        color = "price-up"

    col.markdown(f"""<div class="tradex-box">
        <h4 style="margin:0;">{name}</h4>
        <p class="{color}" style="font-size:18px; margin:10px 0;">{sig}</p>
        <small>LTP: {curr_p:.2f}</small>
    </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
