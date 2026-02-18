import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 
import pandas as pd

st.set_page_config(page_title="TRADEX MEGA TERMINAL", layout="wide")

# --- CUSTOM CSS (Style Restoration) ---
st.markdown("""
    <style>
    .live-clock { font-size: 35px; font-weight: 900; color: #d32f2f; text-align: right; }
    .buy-card { background: #e8f5e9; border: 3px solid #2e7d32; border-radius: 8px; padding: 15px; margin-bottom: 8px; }
    .danger-card { background: #ffebee; border: 3px solid #c62828; border-radius: 8px; padding: 15px; margin-bottom: 8px; animation: blinker 1.5s linear infinite; }
    .compact-card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 8px; border-left: 10px solid #1a237e; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    @keyframes blinker { 50% { opacity: 0.7; } }
    .stock-name { font-size: 24px !important; font-weight: 900; color: #1a237e; margin: 0; }
    .price-bold { font-size: 26px !important; font-weight: 900; color: #000; margin: 0; }
    .signal-label { padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: 900; color: white; text-align: center; width: 85px; }
    .option-card { background: #e3f2fd; border: 2px solid #1565c0; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .buy-level { font-size: 18px; font-weight: 900; color: #1565c0; margin: 0; }
    .tgt-text { color: #2e7d32 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .sl-text { color: #c62828 !important; font-weight: 900; margin: 0; font-size: 16px; }
    .btst-card { background: #f3e5f5; border: 2px solid #4a148c; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_market_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="5d",
