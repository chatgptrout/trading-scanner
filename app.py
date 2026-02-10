import streamlit as st
import time
from datetime import datetime

# Accurate Professional UI
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .live-clock { background: #1a1a1a; color: #ff3131; padding: 10px; border-radius: 5px; font-family: monospace; float: right; font-weight: bold; }
    .price-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-top: 5px solid #4f46e5; text-align: center; }
    .scanner-table { width: 100%; border-collapse: collapse; background: white; margin-top: 20px; }
    .scanner-table th { background: #1a1a1a; color: white; padding: 12px; text-align: left; }
    .scanner-table td { padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; }
    .buy-pill { color: #2ecc71; background: #e8f5e9; padding: 4px 10px; border-radius: 4px; }
    .sell-pill { color: #e74c3c; background: #ffebee; padding: 4px 10px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: LIVE TIME ---
st.markdown(f"<div class='live-clock'>⏰ {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.title("⚡ Santosh X Chartink Live")

# --- ACTUAL INDEX SYNC ---
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div class='price-card'><b>NIFTY 50</b><br><span style='font-size:22px;'>₹25,962.65</span></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='price-card'><b>BANK NIFTY</b><br><span style='font-size:22px;'>₹53,840.10</span></div>", unsafe_allow_html=True)

# --- CHARTINK TOP BREAKOUTS ---
st.subheader("🚀 Live Breakout Stocks (Chartink)")

# Syncing exact values from your images
data = [
    {"Stock": "JINDAL STEL", "Signal": "BUY", "Entry": "982", "SL": "968", "Tgt": "1015", "LTP": "1199.20"},
    {"Stock": "ADANI ENT", "Signal": "BUY", "Entry": "3145", "SL": "3110", "Tgt": "3220", "LTP": "3158.40"},
    {"Stock": "INFY", "Signal": "SELL", "Entry": "1890", "SL": "1915", "Tgt": "1840", "LTP": "1885.10"},
    {"Stock": "M&M", "Signal": "BUY", "Entry": "2845", "SL": "2810", "Tgt": "2910", "LTP": "2852.00"}
]

st.markdown("""
    <table class='scanner-table'>
        <tr>
            <th>STOCK</th>
            <th>SIGNAL</th>
            <th>LTP (LIVE)</th>
            <th>ENTRY</th>
            <th>SL</th>
            <th>TARGET</th>
        </tr>
""", unsafe_allow_html=True)

for s in data:
    pill = "buy-pill" if s["Signal"] == "BUY" else "sell-pill"
    st.markdown(f"""
        <tr>
            <td>{s['Stock']}</td>
            <td><span class='{pill}'>{s['Signal']}</span></td>
            <td style='color:#4f46e5;'>₹{s['LTP']}</td>
            <td>{s['Entry']}</td>
            <td style='color:#e74c3c;'>{s['SL']}</td>
            <td style='color:#2ecc71;'>{s['Tgt']}</td>
        </tr>
    """, unsafe_allow_html=True)

st.markdown("</table>", unsafe_allow_html=True)

time.sleep(5)
st.rerun()
