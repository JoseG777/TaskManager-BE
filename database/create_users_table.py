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

    # drop_table_query = "DROP TABLE IF EXISTS users;"
    # cursor.execute(drop_table_query)
    # conn.commit()
    # print("Table 'users' dropped successfully.")

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'users' created successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn is not None:
        cursor.close()
        conn.close()
        print("Connection closed.")
