import streamlit as st
from database import (get_connection, addCustomer, addFinance)
import pandas as pd

st.title("👨‍💼 Cashier Dashboard")

# ---------- Utility Functions ----------

def fetch_all_products():
    conn = get_connection()
    df = pd.read_sql("SELECT name, quantity, price FROM products", conn)
    conn.close()
    return df

def get_product_info(product_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantity, price FROM products WHERE name = %s", (product_name,))
    result = cur.fetchone()
    conn.close()
    return result

def update_product_quantity(name, quantity_to_deduct):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET quantity = quantity - %s WHERE name = %s", (quantity_to_deduct, name))
    conn.commit()
    conn.close()

# ---------- Page Config and Session State ----------

st.set_page_config("Retail POS System")

if 'page' not in st.session_state:
    st.session_state.page = 'products'

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'customer' not in st.session_state:
    st.session_state.customer = {}

# ---------- Page 1: Add Products ----------

if st.session_state.page == 'products':
    st.title("🛒 Add Products")

    product_df = fetch_all_products()
    product_names = product_df['name'].tolist()

    selected = st.multiselect("Select products", product_names)

    cart = []
    for product in selected:
        available_qty, price = get_product_info(product)
        qty = st.number_input(f"Enter quantity for {product} (Stock: {available_qty})", min_value=0, step=1, key=product)
        if qty > 0:
            if qty > available_qty:
                st.warning(f"❌ Not enough stock for {product}")
            else:
                cart.append({
                    "name": product,
                    "price": float(price),
                    "quantity": int(qty)
                })

    if st.button("Next"):
        if not cart:
            st.warning("Please select at least one product with valid quantity.")
        else:
            st.session_state.cart = cart
            st.session_state.page = 'customer'

# ---------- Page 2: Customer Details ----------

elif st.session_state.page == 'customer':
    st.title("👤 Customer Details")

    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")

    if st.button("Next"):
        if not name or not phone:
            st.warning("Please enter both name and phone.")
        else:
            addCustomer(name, phone)
            st.session_state.customer = {'name': name, 'phone': phone}
            st.session_state.page = 'payment'

    if st.button("⬅️ Back"):
        st.session_state.page = 'products'

# ---------- Page 3: Payment ----------

elif st.session_state.page == 'payment':
    st.title("💳 Payment")

    cart = st.session_state.cart
    total = sum(item['quantity'] * item['price'] for item in cart)
    st.write("### 🧾 Order Summary")
    for item in cart:
        st.write(f"- {item['name']} x {item['quantity']} = ₹{item['quantity'] * item['price']:.2f}")
    st.write(f"### 💰 Total: ₹{total:.2f}")

    method = st.radio("Select Payment Method", ["Cash", "UPI"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Success"):
            addFinance(total)
            for item in cart:
                update_product_quantity(item['name'], item['quantity'])

            st.success("Payment successful and stock updated.")
            st.session_state.page = 'products'
            st.session_state.cart = []
            st.session_state.customer = {}

    with col2:
        if st.button("❌ Cancel"):
            st.session_state.page = 'products'
            st.warning("Transaction canceled. Returning to product page.")
