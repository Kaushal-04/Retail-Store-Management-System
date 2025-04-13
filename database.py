import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        dbname='retail_store',
        user='postgres',
        password='12345',
        port=5432
    )
    cur = conn.cursor()
except Exception as e:
    print("Connection Error")
    print(e)

create_user_table = """CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone_no VARCHAR(10) UNIQUE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Manager', 'Cashier')),
    listed_date DATE NOT NULL DEFAULT CURRENT_DATE
);"""

try:
    cur.execute(create_user_table)
except Exception as e:
    print("Table Exists or Creation Failed")
    print(e)

insert_user = """INSERT INTO users (username, password, full_name, phone_no, role) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (phone_no) DO NOTHING;"""

user_data_manager = ('Kaushal', '123456', 'Kaushal Kumar', '9876543210', 'Manager')
user_data_cashier = ('Raushan', '123', 'Raushan Kumar', '9876543211', 'Cashier')

try:
    cur.execute(insert_user, user_data_manager)
    cur.execute(insert_user, user_data_cashier)
    print("User Added")
except Exception as e:
    print("Error inserting user")
    print(e)
finally:
    conn.commit()
    if cur:
        cur.close()
    if conn:
        conn.close()
