import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

st.set_page_config(page_title="SANTOSH PRO CHART AI", layout="wide")

# Neo-Dark Theme CSS
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; border-radius: 12px; padding: 15px; border-left: 8px solid #00f2ff; margin-bottom: 15px; }</style>""", unsafe_allow_html=True)

# 1. TOP METER (Advance/Decline - image_1000104543.jpg)
st.markdown("<h2 style='color:#00f2ff;'>📊 MARKET BREADTH</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: st.markdown('<div style="background:#00ff88; color:black; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">ADVANCES: 22</div>', unsafe_allow_html=True)
with c2: st.markdown('<div style="background:#ff4b2b; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">DECLINES: 28</div>', unsafe_allow_html=True)

# 2. SELECT STOCK TO VIEW CHART
st.markdown("<h2 style='color:#00f2ff;'>📈 LIVE CHART ANALYSER</h2>", unsafe_allow_html=True)
shikari_list = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "HAL.NS", "DIXON.NS", "TCS.NS"]
selected_stock = st.selectbox("Select Stock to see Live Candles:", shikari_list)

# Fetching Data for Chart
df = yf.download(selected_stock, period='1d', interval='5m', progress=False)
if not df.empty:
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# 3. NEO SIGNALS WITH T1, T2, T3 (image_1000104543.jpg)
st.markdown("<h2 style='color:#00f2ff;'>🚀 LIVE SIGNALS</h2>", unsafe_allow_html=True)
for sym in shikari_list:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        if abs(c) > 0.5:
            color = "#00ff88" if c > 0 else "#ff4b2b"
            action = "SHORT" if c < 0 else "LONG"
            t1 = p * 0.995 if c < 0 else p * 1.005
            t2 = p * 0.990 if c < 0 else p * 1.010
            sl = p * 1.006 if c < 0 else p * 0.994

            st.markdown(f"""
                <div class="card" style="border-left-color:{color}">
                    <h3 style="margin:0;">{action}: {sym} @ ₹{p:.2f} ({c:.2f}%)</h3>
                    <p style="color:{color};"><b>T1: {t1:.2f} | T2: {t2:.2f} | SL: {sl:.2f}</b></p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()
