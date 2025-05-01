# database.py
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "dbname": "retail_store",
    "user": "postgres",
    "password": "12345",
    "port": 5432
}

# ---------- STEP 1: CREATE DATABASE IF NOT EXISTS ----------

def create_database_if_not_exists(dbname="retail_store"):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"Database '{dbname}' created.")
        else:
            print(f"Database '{dbname}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating database:", e)

# ---------- STEP 2: CONNECT TO DATABASE ----------

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print("Database connection failed:", e)
        return None

# ---------- STEP 3: TABLE CREATION ----------

def create_user_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(100),
        phone_no VARCHAR(10) UNIQUE,
        role VARCHAR(20) NOT NULL CHECK (role IN ('Manager', 'Cashier')),
        listed_date DATE NOT NULL DEFAULT CURRENT_DATE
    );
    """
    execute_query(query)

def create_customer_table():
    query = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(10) UNIQUE NOT NULL
    );
    """
    execute_query(query)

def create_product_table():
    query = """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        quantity INTEGER NOT NULL CHECK (quantity >= 0),
        price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
    );
    """
    execute_query(query)

def create_finance_table():
    query = """
    CREATE TABLE IF NOT EXISTS finance (
        transaction_id SERIAL PRIMARY KEY,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0)
    );
    """
    execute_query(query)

# ---------- STEP 4: DATA FUNCTIONS ----------

def addUser(username, password, full_name, phone_no, role):
    query = """
    INSERT INTO users (username, password, full_name, phone_no, role)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (phone_no) DO NOTHING;
    """
    execute_query(query, (username, password, full_name, phone_no, role))

def addCustomer(name, phone_number):
    query = """
    INSERT INTO customers (name, phone_number)
    VALUES (%s, %s)
    ON CONFLICT (phone_number) DO NOTHING;
    """
    execute_query(query, (name, phone_number))

def addProduct(name, quantity, price):
    query = """
    INSERT INTO products (name, quantity, price)
    VALUES (%s, %s, %s)
    ON CONFLICT (name) DO UPDATE
    SET quantity = EXCLUDED.quantity,
        price = EXCLUDED.price;
    """
    execute_query(query, (name, quantity, price))

def updateProduct(name, new_quantity, new_price):
    query = """
    UPDATE products
    SET quantity = %s, price = %s
    WHERE name = %s;
    """
    execute_query(query, (new_quantity, new_price, name))

def addFinance(amount):
    query = """
    INSERT INTO finance (amount)
    VALUES (%s);
    """
    execute_query(query, (amount,))

# ---------- STEP 5: QUERY EXECUTOR ----------

def execute_query(query, values=None):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, values)
                conn.commit()
        except Exception as e:
            print("Query Execution Error:", e)
        finally:
            conn.close()

# ---------- STEP 6: RUN EVERYTHING ----------

if __name__ == "__main__":
    print("Initializing database and tables...")
    create_database_if_not_exists("retail_store")

    create_user_table()
    create_customer_table()
    create_product_table()
    create_finance_table()

    print("✅ Tables created.")

    print("📥 Inserting sample data...")

    addUser("Kaushal", "123456", "Kaushal Kumar", "9876543210", "Manager")
    addUser("Raushan", "123", "Raushan Kumar", "9876543211", "Cashier")
    addCustomer("Amit Kumar", "9876543212")
    addProduct("Soap", 100, 20.5)
    updateProduct("Soap", 80, 19.99)
    addFinance(399.50)

    print("✅ Sample data inserted successfully.")
