import streamlit as st
from fetch_from_db import fetch_role
import os

st.title("Retail Store Management System")

user_name = st.text_input("ID")
password = st.text_input("Password", type="password")
    
login_button = st.button("Login")

if login_button:
    if user_name != "" and password != "":
        user_data = fetch_role(user_name)
        username_db, password_db, role_db = user_data
        if(username_db == user_name and password_db == password):
            if(role_db == "Manager"):
                os.system("streamlit run pages/manager.py")
            else:
                os.system("streamlit run pages/cashier.py")
        else:
            st.error("Invalid ID or Password.")
    else:
        st.error("Invalid ID or Password.")
