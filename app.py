import streamlit as st
import requests

st.title("SANTOSH SCANNER")

# Sidebar inputs
client_id = st.sidebar.text_input("Dhan Client ID")
token = st.sidebar.text_input("Dhan Token", type="password")

if client_id and token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {
            'access-token': token,
            'client-id': client_id,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "instruments": [
                {
                    "symbol": "CRUDEOIL FEB FUT",
                    "exchange": "MCX",
                    "instrument_type": "FUTCOM",
                    "security_id": "63"
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            price_dict = data.get('data', {})
            if price_dict:
                price = list(price_dict.values())[0]
                st.header(f"CRUDE OIL: Rs {price}")
                st.success("LIVE MATCHED")
            else:
                st.warning("Data empty. Check 'Data APIs' switch in Dhan Profile.")
        else:
            st.error(f"Dhan Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Enter Client ID and Token in Sidebar")
