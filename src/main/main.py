from flask import Flask
from flask_restful import Resource, Api, request

import room
import room_by_id
import storey
import storey_by_id
import building
import building_by_id


app = Flask(__name__)
api = Api(app)


class Room(Resource):

    def get(self):
        include_deleted = request.args.get("include_deleted")
        storey_id = request.args.get("storey_id")
        return room.handle_get(include_deleted, storey_id)

    def post(self):
        data = request.json
        name = data.get("name")
        storey_id = data.get("storey_id")
        return room.handle_post(name, storey_id)


class RoomById(Resource):

    def get(self, room_id):
        return room_by_id.handle_get(room_id)

    def put(self, room_id):
        data = request.json
        name = data.get("name")
        storey_id = data.get("storey_id")
        if "deleted_at" in list(data.keys()):
            deleted_at = None
        else:
            deleted_at = 1
        return room_by_id.handle_put(room_id, name, storey_id, deleted_at)

    def delete(self, room_id):
        return room_by_id.handle_delete(room_id)


class Storey(Resource):

    def get(self):
        include_deleted = request.args.get("include_deleted")
        building_id = request.args.get("building_id")
        return storey.handle_get(include_deleted, building_id)

    def post(self):
        data = request.json
        name = data.get("name")
        building_id = data.get("building_id")
        return room.handle_post(name, building_id)


class StoreyById(Resource):

    def get(self, storey_id):
        return storey_by_id.handle_get(storey_id)

    def put(self, storey_id):
        data = request.json
        name = data.get("name")
        building_id = data.get("building_id")
        if "deleted_at" in list(data.keys()):
            deleted_at = None
        else:
            deleted_at = 1
        return storey_by_id.handle_put(storey_id, name, building_id, deleted_at)

    def delete(self, storey_id):
        return storey_by_id.handle_delete(storey_id)


class Building(Resource):
    
    def get(self):
        include_deleted = request.args.get("include_deleted")
        return building.handle_get(include_deleted)
    
    def post(self):
        data = request.json
        name = data.get("name")
        address = data.get("address")
        return building.handle_post(name, address)


class BuildingById(Resource):

    def get(self, building_id):
        return building_by_id.handle_get(building_id)

    def put(self, building_id):
        data = request.json
        name = data.get("name")
        address = data.get("address")
        if "deleted_at" in list(data.keys()):
            deleted_at = None
        else:
            deleted_at = 1
        return building_by_id.handle_put(building_id, name, address, deleted_at)

    def delete(self, building_id):
        return building_by_id.handle_delete(building_id)
    

api.add_resource(Room, '/api/v2/assets/rooms')
api.add_resource(RoomById, '/api/v2/assets/rooms/<string:room_id>')
api.add_resource(Storey, '/api/v2/assets/storeys')
api.add_resource(StoreyById, '/api/v2/assets/storeys/<string:storey_id>')
api.add_resource(Building, '/api/v2/assets/buildings')
api.add_resource(BuildingById, '/api/v2/assets/buildings/<string:building_id>')


if __name__ == '__main__':
    app.run(debug=True)
