import os

import psycopg2


def get_connection():
    conn = psycopg2.connect(host='localhost',
                            database='assets',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


def select(columns, table, where="1 = 1"):
    conn = get_connection()
    cursor = conn.cursor()

    query = "select {} from {} where {}".format(columns, table, where)
    print (query)
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result


def insert(table, values):
    conn = get_connection()
    cursor = conn.cursor()

    #columns = "%s" + ", %s" * (len(values) - 1)
    query = "insert into {} values({})".format(table, values)
    cursor.execute(query, values)

    conn.close()
