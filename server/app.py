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
    
    def post(self):
        data=request.get_json()

        new_scientist = Scientist(
            name= data['name'],
            field_of_study= data['field_of_study']
        )

        db.session.add(new_scientist)
        db.session.commit()

        return make_response(new_scientist.to_dict(), 201)


class IndividualScientist(Resource):
    def get(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if scientist:
            return make_response(scientist.to_dict(), 200)
        return make_response({'error': 'Scientist not found'}, 400)
    
    def patch(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(scientist, attr, data[attr])
        db.session.add(scientist)
        db.session.commit()
        response = scientist.to_dict()
        return make_response(response, 200)
    
    def delete(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if scientist:
            db.session.delete(scientist)
            db.session.commit()
            return make_response({}, 200)
        return make_response({'error': 'Scientist not found'}, 404)


class Planets(Resource):
    def get(self):
        planet_index = []
        for planet in Planet.query.all():
            planet_dict = {
                "id": planet.id,
                "name": planet.name,
                "distance_from_earth": planet.distance_from_earth,
                "nearest_star": planet.nearest_star
            }
            planet_index.append(planet_dict)
        return make_response(planet_index, 200)

api.add_resource(Scientists, '/scientists')
api.add_resource(IndividualScientist, '/scientists/<int:id>')
api.add_resource(Planets, '/planets')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
