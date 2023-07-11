#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):
        scientist_index = []
        for scientist in Scientist.query.all():
            sci_dict = {
                'id': scientist.id,
                'name': scientist.name,
                'field_of_study': scientist.field_of_study
            }
            scientist_index.append(sci_dict)
        return make_response(scientist_index, 200)

class IndividualScientist(Resource):
    def get(self, id):
        return make_response(
            Scientist.query.filter(Scientist.id == id).first().to_dict(),
            200
        )

api.add_resource(Scientists, '/scientists')
api.add_resource(IndividualScientist, '/scientists/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
