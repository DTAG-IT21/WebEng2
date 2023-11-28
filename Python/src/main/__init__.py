from flask import Flask
from flask import request
from flask_restful import Resource, Api

import room

app = Flask(__name__)
api = Api(app)


class Room(Resource):

    def get(self):
        include_deleted = request.args.get("include_deleted")
        storey_id = request.args.get("storey_id")
        return room.handle_get(include_deleted, storey_id)

    def post(self):
        name = request.args.get("name")
        storey_id = request.args.get("storey_id")
        return room.handle_post(name, storey_id)


class RoomById(Resource):
    def get(self, id):
        return
        # TODO

    def put(self, id):
        return
        # TODO

    def delete(self, id):
        return
        # TODO


api.add_resource(Room, '/api/v2/assets/rooms')
api.add_resource(RoomById, '/api/v2/assets/rooms/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
