import os
import psycopg2
from contextlib import contextmanager


@contextmanager
def get_connection():

    conn = psycopg2.connect(host=os.getenv("POSTGRES_ASSETS_HOST"),
                            port=os.getenv("POSTGRES_ASSETS_PORT"),
                            database=os.getenv("POSTGRES_ASSETS_DBNAME"),
                            user=os.getenv("POSTGRES_ASSETS_USER"),
                            password=os.getenv("POSTGRES_ASSETS_PASSWORD"))
    try:
        yield conn
    finally:
        conn.close()


def test_connection():
    try:
        with get_connection():
            return True
    except psycopg2.OperationalError as e:
        return e
