from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('building_id')

class Building:

    def get(self):
        args = parser.parse_args()


api.add_resource(Building, '/building')

if __name__ == '__main__':
    app.run(debug=True)
