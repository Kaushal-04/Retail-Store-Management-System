import streamlit as st
import pandas as pd
from datetime import date

from database import get_connection, addProduct, updateProduct

st.title("👨‍💼 Manager Dashboard")

menu = st.sidebar.radio("Select Action", [
    "Add or Update Product",
    "Update Product Details",
    "View Customers by Date",
    "View Finance by Date"
])

# 1. Add or Update Product
if menu == "Add or Update Product":
    st.header("📦 Add or Update Product")

    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.1)

    if st.button("Add / Update Product"):
        if not name or quantity <= 0 or price <= 0:
            st.warning("Please fill all fields with valid values.")
        else:
            addProduct(name, quantity, price)
            st.success(f"Product '{name}' added or updated successfully.")

# 2. Update Product Details
elif menu == "Update Product Details":
    st.header("✏️ Update Product Price or Quantity")

    conn = get_connection()
    df = pd.read_sql("SELECT name, quantity, price FROM products", conn)
    conn.close()

    if df.empty:
        st.info("No products available.")
    else:
        selected_product = st.selectbox("Select Product to Update", df["name"].tolist())
        current_data = df[df["name"] == selected_product].iloc[0]

        new_quantity = st.number_input("New Quantity", min_value=0, value=int(current_data['quantity']), step=1)
        new_price = st.number_input("New Price", min_value=0.0, value=float(current_data['price']), step=0.1)

        if st.button("Update Product"):
            updateProduct(selected_product, new_quantity, new_price)
            st.success(f"{selected_product} updated successfully.")

# 3. View Customers (All, Searchable)
elif menu == "View Customers by Date":
    st.header("👥 View All Customers")

    search_query = st.text_input("🔍 Search by Customer Name")

    conn = get_connection()
    try:
        query = "SELECT * FROM customers;"
        df = pd.read_sql(query, conn)

        # Filter by search query if provided
        if search_query:
            df = df[df['name'].str.contains(search_query, case=False)]

        if df.empty:
            st.info("No customers found.")
        else:
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error fetching customer data: {e}")
    finally:
        conn.close()



# 4. View Finance by Date
elif menu == "View Finance by Date":
    st.header("💰 View Finance Records by Date")

    start_date = st.date_input("Start Date", value=date.today(), key="fstart")
    end_date = st.date_input("End Date", value=date.today(), key="fend")

    if st.button("Fetch Finance Data"):
        query = """
        SELECT * FROM finance
        WHERE DATE(date) BETWEEN %s AND %s;
        """
        conn = get_connection()
        try:
            df = pd.read_sql(query, conn, params=(start_date, end_date))
            if df.empty:
                st.info("No finance records found.")
            else:
                st.dataframe(df)
                st.write(f"### Total Income: ₹{df['amount'].sum():.2f}")
        except Exception as e:
            st.error(f"Error fetching finance data: {e}")
        finally:
            conn.close()