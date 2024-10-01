import json
import pg8000 # can be switched out, was just easier for lambda functions
import os
import re

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT', '5432')

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def connect_to_db():
    return pg8000.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=int(DB_PORT)
    )

def lambda_handler(event, context):
    conn = None
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')

        if not email or not is_valid_email(email):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'message': 'Invalid email format'})
            }

        conn = connect_to_db()
        cursor = conn.cursor()

        insert_query = '''
        INSERT INTO users (email, created_at)
        VALUES (%s, NOW())
        RETURNING id;
        '''
        cursor.execute(insert_query, (email,))
        conn.commit()

        user_id = cursor.fetchone()[0]

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'User added successfully',
                'user_id': user_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Error adding user',
                'error': str(e)
            })
        }

    finally:
        if conn:
            cursor.close()
            conn.close()
