import streamlit as st
from dhanhq import dhanhq

st.title("🚀 SMART SCANNER")

# Sidebar for Token
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Dhan connect - 100% Asli Client ID
        dhan = dhanhq("1106004757", token) 
        
        # Crude Oil Data Fetch
        # Instrument type 'FUTCOM' for MCX Crude
        data = dhan.get_ltp_data([{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}])
        
        if data.get('status') == 'success':
            price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 0)
            st.metric("CRUDE OIL FEB FUT", f"₹{price}")
            st.success("✅ LIVE MATCHED!")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("👈 Please enter your Dhan Token in the sidebar")
