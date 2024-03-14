import os
import uuid
import logging
import requests

from flask import Flask
from flask_restful import Resource, Api, request
from jose import jwt
from logging.config import dictConfig

from src.assets import room, room_by_id, storey, storey_by_id, building, building_by_id
import src.main.response_generator as response_generator
import src.main.database as database


loglevel = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': loglevel.get(os.getenv("LOGLEVEL"), logging.INFO),
        'handlers': ['wsgi'],
    }
})


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
            storey_id = request.args.get("storey_id", "1")
            if is_uuid(storey_id) or storey_id is None:
                response = room.handle_get(include_deleted, storey_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid storey id"
                more_info = "The given storey id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def post(self):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            storey_id = data.get("storey_id")
            if is_uuid(storey_id):
                response = room.handle_post(name, storey_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid storey id"
                more_info = "The given storey id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

    class RoomById(Resource):

        def get(self, room_id):
            if is_uuid(room_id):
                response = room_by_id.handle_get(room_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid room id"
                more_info = "The given room id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def put(self, room_id):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            storey_id = data.get("storey_id")
            if is_uuid(room_id) and is_uuid(storey_id):
                if "deleted_at" in list(data.keys()):
                    deleted_at = None
                else:
                    deleted_at = 1
                response = room_by_id.handle_put(room_id, name, storey_id, deleted_at)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid room id or storey id"
                more_info = "The given room id or storey id are not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def delete(self, room_id):
            if is_uuid(room_id):
                response = room_by_id.handle_delete(room_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid room id"
                more_info = "The given room id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

    class Storey(Resource):

        def get(self):
            include_deleted = request.args.get("include_deleted")
            building_id = request.args.get("building_id", "1")
            if is_uuid(building_id):
                response = storey.handle_get(include_deleted, building_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid building id"
                more_info = "The given building id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def post(self):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            building_id = data.get("building_id")
            if is_uuid(building_id):
                response = storey.handle_post(name, building_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid building id"
                more_info = "The given building id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

    class StoreyById(Resource):

        def get(self, storey_id):
            if is_uuid(storey_id):
                response = storey_by_id.handle_get(storey_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid storey id"
                more_info = "The given storey id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def put(self, storey_id):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            building_id = data.get("building_id")
            if is_uuid(storey_id) and is_uuid(building_id):
                if "deleted_at" in list(data.keys()):
                    deleted_at = None
                else:
                    deleted_at = 1
                response = storey_by_id.handle_put(storey_id, name, building_id, deleted_at)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid storey id or building_id"
                more_info = "The given storey id or building_id are not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def delete(self, storey_id):
            if is_uuid(storey_id):
                response = storey_by_id.handle_delete(storey_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid storey id"
                more_info = "The given storey id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

    class Building(Resource):

        def get(self):
            include_deleted = request.args.get("include_deleted")
            response = building.handle_get(include_deleted)
            app.logger.debug("Response: " + str(response.json))
            return response

        def post(self):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            address = data.get("address")
            response = building.handle_post(name, address)
            app.logger.debug("Response: " + str(response.json))
            return response

    class BuildingById(Resource):

        def get(self, building_id):
            if is_uuid(building_id):
                response = building_by_id.handle_get(building_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid building id"
                more_info = "The given building id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def put(self, building_id):
            data = request.json
            app.logger.debug("Request: " + str(data))
            name = data.get("name")
            address = data.get("address")
            if is_uuid(building_id):
                if "deleted_at" in list(data.keys()):
                    deleted_at = None
                else:
                    deleted_at = 1
                response = building_by_id.handle_put(building_id, name, address, deleted_at)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid building id"
                more_info = "The given building id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

        def delete(self, building_id):
            if is_uuid(building_id):
                response = building_by_id.handle_delete(building_id)
                app.logger.debug("Response: " + str(response.json))
                return response
            else:
                message = "Invalid building id"
                more_info = "The given building_id is not in uuid format"
                response = response_generator.error_response(message, more_info)
                app.logger.debug("Response: " + str(response.json))
                return response

    @app.route('/api/v2/assets/status', methods=['GET'])
    def status():
        response = {
            "authors": [
                "Nico Merkel",
                "Leon Richter"
            ],
            "api_version": "2.0.0"
        }
        app.logger.debug("Response: " + str(response_generator.response_body(response, 200).json))
        return response_generator.response_body(response, 200)

    @app.route('/api/v2/assets/health/ready', methods=['GET'])
    def ready():
        response = {
            "ready": True
        }
        app.logger.debug("Response: " + str(response_generator.response_body(response, 200).json))
        return response_generator.response_body(response, 200)

    @app.route('/api/v2/assets/health/live', methods=['GET'])
    def live():
        if database.test_connection():
            app.logger.debug("Response: " + str(response_generator.response_body({'live': True}, 200).json))
            return response_generator.response_body({'live': True}, 200)
        else:
            response = {
                'live': False,
            }
            app.logger.debug("Response: " + str(response_generator.response_body(response, 500).json))
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
            app.logger.debug("Response: " + str(response_generator.response_body(response, 500).json))
            return response_generator.response_body(response, 500)
        else:
            app.logger.debug("Response: " + str(response_generator.response_body(response, 200).json))
            return response_generator.response_body(response, 200)

    @app.route('/api/v2/assets/log/<string:level>', methods=['GET'])
    def log_level(level):
        if level not in loglevel:
            level = app.logger.getEffectiveLevel()
        app.logger.setLevel(loglevel.get(level, level))
        app.logger.critical("LogLevel set to: " + level)
        response = {
            "message": "LogLevel set to: " + level
        }
        return response_generator.response_body(response, 200)

    api.add_resource(Room, '/api/v2/assets/rooms')
    api.add_resource(RoomById, '/api/v2/assets/rooms/<string:room_id>')
    api.add_resource(Storey, '/api/v2/assets/storeys')
    api.add_resource(StoreyById, '/api/v2/assets/storeys/<string:storey_id>')
    api.add_resource(Building, '/api/v2/assets/buildings')
    api.add_resource(BuildingById, '/api/v2/assets/buildings/<string:building_id>')

    return app


def is_uuid(candidate):
    try:
        uuid_obj = uuid.UUID(candidate)
        return str(uuid_obj) == candidate
    except ValueError:
        return False


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=9000)

