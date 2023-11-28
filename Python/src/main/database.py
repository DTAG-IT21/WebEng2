import os

import psycopg2


def get_connection():
    conn = psycopg2.connect(host='localhost',
                            database='assets',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn
