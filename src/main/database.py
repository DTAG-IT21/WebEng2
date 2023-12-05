import os
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = psycopg2.connect(host='localhost',
                            port=os.environ['POSTGRES_ASSETS_PORT'],
                            database=os.environ['POSTGRES_ASSETS_DBNAME'],
                            user=os.environ['POSTGRES_ASSETS_USER'],
                            password=os.environ['POSTGRES_ASSETS_PASSWORD'])
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_cursor(conn):
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def test_connection():
    try:
        with get_connection():
            return True
    except psycopg2.OperationalError:
        return False


def select(columns, table, where="1 = 1"):
    with get_connection() as conn:
        with get_cursor(conn) as cursor:
            query = f"""SELECT {columns} FROM {table} WHERE {where}"""
            cursor.execute(query)
            result = cursor.fetchall()
    return result


def insert(table, values):
    with get_connection() as conn:
        with get_cursor(conn) as cursor:
            query = f"""INSERT INTO {table} VALUES({values})"""
            cursor.execute(query)
            conn.commit()


def update(table, values, where):
    with get_connection() as conn:
        with get_cursor(conn) as cursor:
            query = f"""UPDATE {table} SET {values} WHERE {where}"""
            cursor.execute(query)
            conn.commit()


def delete(table, where):
    def update(table, values, where):
        with get_connection() as conn:
            with get_cursor(conn) as cursor:
                query = f"""DELETE FROM {table} WHERE {where}"""
                cursor.execute(query)
                conn.commit()
