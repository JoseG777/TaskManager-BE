import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST').strip()
DB_NAME = os.getenv('DB_NAME').strip()
DB_USER = os.getenv('DB_USER').strip()
DB_PASSWORD = os.getenv('DB_PASS').strip()
DB_PORT = os.getenv('DB_PORT', '5432').strip()

conn = None

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Connected to the database successfully.")

    
    select_query = "SELECT * FROM users;"
    cursor.execute(select_query)

    
    users = cursor.fetchall()

    
    print("Users in the database:")
    for user in users:
        print(user)

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn is not None:
        cursor.close()
        conn.close()
        print("Connection closed.")
