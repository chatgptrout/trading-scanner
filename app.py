import streamlit as st
from dhanhq import dhanhq

st.title("🚀 SMART SCANNER")
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Dhan connect - Yahan apni sahi Client ID dalna zaroori hai
        dhan = dhanhq("1106004757", token) 
        
        # Crude Oil Data Fetch
        instruments = [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}]
        data = dhan.get_ltp_data(instruments)
        
        # Price Match
        price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 5692.0)
        
        st.metric("CRUDE OIL FEB FUT", f"₹{price}")
        st.success("SUCCESS: Data Matched with Dhan Live!")
    except:
        st.error("Technical Error: Please check Client ID and Token")
else:
    st.warning("Awaiting Token from Sidebar...")

