import streamlit as st

st.title("Retail Store Management System")

user_id = st.text_input("ID")
password = st.text_input("Password", type="password")
    
login_button = st.button("Login")

if login_button:
    if user_id == "Kaushal" and password == "123456":
        st.success("Login successful!")
    else:
        st.error("Invalid ID or Password.")
