import streamlit as st
import requests

st.title("SANTOSH SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Market Feed URL
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        
        # Sabse simple symbol format jo Dhan accept karta hai
        payload = {
            "instruments": [
                {"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            price_data = data.get('data', {})
            # Agar dictionary khali nahi hai toh price dikhao
            if price_data:
                # 'MCX:CRUDEOIL FEB FUT' key se data nikalna
                price = price_data.get('MCX:CRUDEOIL FEB FUT', 0)
                st.header(f"CRUDE OIL: Rs {price}")
                st.success("LIVE MATCHED")
            else:
                st.warning("Dhan returned empty data. Check if 'Data APIs' is ON in Dhan Profile.")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Paste 'OfficeScanner' Token in Sidebar")
