import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH HEATMAP PRO", layout="wide")

# Dark Theme
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ff4b2b;'>🟥 MARKET HEATMAP (DEEP RED STYLE)</h1>", unsafe_allow_html=True)

# Stocks to track (Jaise Pharma list aapne bheji)
watchlist = [
    "SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", 
    "LUPIN.NS", "TATASTEEL.NS", "RELIANCE.NS", "SBIN.NS",
    "ZOMATO.NS", "ADANIENT.NS", "TCS.NS", "INFY.NS"
]

def get_heatmap_data():
    data = []
    for sym in watchlist:
        try:
            t = yf.Ticker(sym).fast_info
            price = t['last_price']
            change = ((price - t['previous_close']) / t['previous_close']) * 100
            data.append({"Symbol": sym.replace(".NS", ""), "Price": price, "Change": change})
        except: continue
    return pd.DataFrame(data)

df = get_heatmap_data()

if not df.empty:
    # 1000104630.jpg jaisa Treemap logic
    fig = px.treemap(
        df, 
        path=['Symbol'], 
        values=[abs(x) for x in df['Change']], # Bada change = Bada box
        color='Change',
        color_continuous_scale=['#ff0000', '#ff4b2b', '#333333', '#00ff88'], # Red to Green
        custom_data=['Price', 'Change']
    )

    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=600,
        template="plotly_dark"
    )
    
    fig.update_traces(
        texttemplate="<br><b>%{label}</b><br>₹%{customdata[0]:.2f}<br>%{customdata[1]:.2f}%",
        textfont_size=18
    )

    st.plotly_chart(fig, use_container_width=True)

st.info("💡 Bada Box = Bada Movement | Deep Red = Heavy Selling")

time.sleep(30)
st.rerun()
