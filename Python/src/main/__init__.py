from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import psycopg2

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('building_id')


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='RoomManager',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


class Building:

    def get(self):
        args = parser.parse_args()
        conn = get_db_connection()


api.add_resource(Building, '/building')

if __name__ == '__main__':
    app.run(debug=True)
