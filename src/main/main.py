import os
import sys

import requests
from flask import Flask
from flask_restful import Resource, Api, request
from jose import jwt

sys.path.append('../src')
from src.assets import room, room_by_id, storey, storey_by_id, building, building_by_id
import response_generator
import database


def create_app():
    app = Flask(__name__)

    api = Api(app)

    keycloak_url = f'http://{os.getenv("KEYCLOAK_HOST")}/auth/realms/{os.getenv("KEYCLOAK_REALM")}'

    @app.route('/api/v2/assets/verify', methods=["POST"])
    def verify_token():
        token = request.json['token']
        public_key = get_keycloak_public_key()

        try:
            payload = jwt.decode(token, public_key, algorithms=['RS256'])
            return payload, 200
        except Exception as e:
            return str(e), 400

    def get_keycloak_public_key():
        response = requests.get(f'{keycloak_url}')

        public_key_data = response.json()['public_key']
        print(public_key_data)
        public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key_data}\n-----END PUBLIC KEY-----"

        return public_key

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

    @app.route('/api/v2/assets/status', methods=['GET'])
    def status():
        response = {
            "authors": [
                "Nico Merkel",
                "Leon Richter"
            ],
            "api_version": "2.0.0"
        }
        return response_generator.response_body(response, 200)

    @app.route('/api/v2/assets/health/ready', methods=['GET'])
    def ready():
        response = {
            "ready": True
        }
        return response_generator.response_body(response, 200)

    @app.route('/api/v2/assets/health/live', methods=['GET'])
    def live():
        if database.test_connection():
            return response_generator.response_body({'live': True}, 200)
        else:
            response = {
                'live': False,
            }
            return response_generator.response_body(response, 500)

    @app.route('/api/v2/assets/health', methods=['GET'])
    def health():
        is_ready = ready().get_json()
        is_live = live().get_json()

        is_ready = is_ready['ready']
        is_live = is_live['live']

        response = {
            'ready': is_ready,
            'live': is_live
        }

        if not is_ready or not is_live:
            return response_generator.response_body(response, 500)
        else:
            return response_generator.response_body(response, 200)

    api.add_resource(Room, '/api/v2/assets/rooms')
    api.add_resource(RoomById, '/api/v2/assets/rooms/<string:room_id>')
    api.add_resource(Storey, '/api/v2/assets/storeys')
    api.add_resource(StoreyById, '/api/v2/assets/storeys/<string:storey_id>')
    api.add_resource(Building, '/api/v2/assets/buildings')
    api.add_resource(BuildingById, '/api/v2/assets/buildings/<string:building_id>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
