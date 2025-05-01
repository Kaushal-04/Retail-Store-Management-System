import psycopg2
def fetch_role(user_name):
    try:
        conn = psycopg2.connect(
            host='localhost',
            dbname='retail_store',
            user='postgres',
            password='12345',
            port=5432
        )
        cur = conn.cursor()
        query = "SELECT username, password, role FROM users WHERE username = %s"
        cur.execute(query, (user_name,))
        user_data = cur.fetchone()
        return user_data
    
    except Exception as e:
        print("Connection Error")
        print(e)
    finally:
        conn.commit()
        if cur:
            cur.close()
        if conn:
            conn.close()
