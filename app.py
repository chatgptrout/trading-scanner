import streamlit as st
import requests

st.title("SANTOSH SCANNER")

token = st.sidebar.text_input("Dhan Token", type="password")

if token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {
            'access-token': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Crude Oil Feb Fut (Security ID 63) - No Emojis, No Extra Text
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
                # Direct value extraction
                price = list(price_dict.values())[0]
                st.header(f"CRUDE OIL: Rs {price}")
                st.success("LIVE MATCHED")
            else:
                st.warning("Connected but No Data. Check 'Data APIs' toggle in Dhan Profile.")
        else:
            st.error(f"Dhan Status: {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Paste 'OfficeScanner' Token in Sidebar")
