import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --- CUSTOM CSS FOR DARK TERMINAL LOOK ---
st.markdown("""
    <style>
    .reportview-container { background: #121212; color: white; }
    .stTable { font-size: 12px; }
    .buy-row { background-color: #1b5e20; color: white; }
    .sell-row { background-color: #b71c1c; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- TOP INDEX BAR ---
st.markdown("""
    <div style='background: black; padding: 5px; border: 1px solid #444; color: orange;'>
        NIFTY 50: <span style='color:red;'>17412.9 (-1.00%)</span> | 
        BANK NIFTY: <span style='color:red;'>40485.45 (-1.87%)</span> | 
        GOLD: <span style='color:blue;'>56130 (1.50%)</span>
    </div>
""", unsafe_allow_html=True)

# --- FUNCTION TO CREATE SECTIONS ---
def trade_section(title, data):
    st.markdown(f"<div style='background:#444; padding:2px; font-weight:bold;'>{title}</div>", unsafe_allow_html=True)
    st.table(data)

# --- SAMPLE DATA (BASED ON MOTILAL TERMINAL) ---
intraday_data = pd.DataFrame([
    {"Action": "BUY EXIT", "Name": "NIFTY 50", "Entry": 17420, "SL": 17298, "CMP": 17411, "Target": 17576, "Status": "Long Exit"},
    {"Action": "BUY", "Name": "GOLD", "Entry": 56180, "SL": 55983, "CMP": 56130, "Target": 56651, "Status": "Stop"}
])

# --- DISPLAY SECTIONS ---
trade_section("INTRADAY - Trading For Few Hours", intraday_data)
# Add similar sections for SWING and MOMENTUM
