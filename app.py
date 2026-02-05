import streamlit as st
from dhanhq import dhanhq
import time

st.set_page_config(page_title="Split Market Scanner", layout="centered")

# --- UI DESIGN ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: white; }
    .card { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #333; margin-bottom: 15px; }
    .price-val { font-size: 40px; font-weight: bold; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Mobile Token
with st.sidebar:
    st.header("🔑 Mobile Token")
    user_token = st.text_input("Paste Token Here", type="password")
    client_id = "1106004757"

st.title("🔍 SMART SCANNER")

# --- TABS CREATION (Equity aur Commodity ko alag karne ke liye) ---
tab1, tab2 = st.tabs(["📈 STOCKS (Equity)", "🛢️ COMMODITY"])

if user_token:
    try:
        dhan = dhanhq(client_id, user_token)
        
        with tab1:
            st.subheader("Nifty 1000 Breakouts")
            # Yahan sirf Stocks dikhenge
            stocks = [{"name": "DIXON", "price": 11250, "rsi": 68}, {"name": "TATASTEEL", "price": 162, "rsi": 45}]
            for s in stocks:
                st.markdown(f'<div class="card"><h3>{s["name"]}</h3><div class="price-val">₹ {s["price"]}</div><p>RSI: {s["rsi"]}</p></div>', unsafe_allow_html=True)

        with tab2:
            st.subheader("Crude & Metals")
            # Yahan sirf Commodity dikhegi
            commodities = [{"name": "CRUDE OIL", "price": 6450, "rsi": 62}, {"name": "GOLD GUINEA", "price": 48200, "rsi": 35}]
            for c in commodities:
                st.markdown(f'<div class="card"><h3>{c["name"]}</h3><div class="price-val">₹ {c["price"]}</div><p>RSI: {c["rsi"]}</p></div>', unsafe_allow_html=True)

    except:
        st.error("Token Error! Mobile se update karein.")
else:
    st.warning("Awaiting Token from Sidebar...")

time.sleep(30)
st.rerun()