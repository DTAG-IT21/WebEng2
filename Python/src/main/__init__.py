from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import os
import psycopg2

import room

app = Flask(__name__)
api = Api(app)


class Room(Resource):

    def get(self):
        include_deleted = request.args.get("include_deleted")
        return room.handle_get(include_deleted)


api.add_resource(Room, 'api/v2/assets/rooms')

if __name__ == '__main__':
    app.run(debug=True)
