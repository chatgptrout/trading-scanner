import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

# PC ke liye wide layout aur desktop title
st.set_page_config(page_title="SANTOSH PC COMMANDER", layout="wide")

st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; padding: 15px; border-radius: 10px; border: 1px solid #ffcc00; }</style>""", unsafe_allow_html=True)

# 1. LIVE DATA FOR ALL STOCKS
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS", "TCS.NS"]

def get_pc_data():
    data = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            data.append({
                "Symbol": s.replace(".NS",""), "Full": s, 
                "Price": t['last_price'], 
                "Change": ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100
            })
        except: continue
    return pd.DataFrame(data)

df = get_pc_data()

# 2. PC DASHBOARD LAYOUT (Side-by-Side)
col_left, col_right = st.columns([1, 2]) # 1 part Heatmap, 2 parts Chart

with col_left:
    st.markdown("<h3 style='color:#ff4b2b;'>🟥 MARKET HEATMAP</h3>", unsafe_allow_html=True)
    fig_map = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                         color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                         custom_data=['Full'])
    fig_map.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=600, template="plotly_dark")
    # Click selection for PC
    selected = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun", key="pc_map")

with col_right:
    # Selection logic
    active_stock = "SUNPHARMA.NS"
    if selected and "selection" in selected and selected["selection"]["points"]:
        active_stock = selected["selection"]["points"][0]["customdata"][0]
    
    st.markdown(f"<h3 style='color:#00f2ff;'>📈 LIVE CHART: {active_stock}</h3>", unsafe_allow_html=True)
    try:
        h = yf.Ticker(active_stock).history(period='1d', interval='5m')
        chart = go.Figure(data=[go.Candlestick(x=h.index, open=h['Open'], high=h['High'], low=h['Low'], close=h['Close'],
                                             increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b')])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=600, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True, key=f"pc_chart_{active_stock}")
    except:
        st.error("Select a box on the left to load chart.")

# 3. BOTTOM INFO BAR
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1: st.success(f"NIFTY 50: {yf.Ticker('^NSEI').fast_info['last_price']:.2f}")
with c2: st.info(f"Active Scan: {active_stock}")
with c3: st.warning("Data: Live (5m Interval)")
with c4: st.write(f"Refreshed: {time.strftime('%H:%M:%S')}")

time.sleep(20)
st.rerun()
