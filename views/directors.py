from flask import request
from flask_restx import Resource, Namespace

from helpers.container import director_service
from dao.model.director import DirectorSchema
from helpers.decorators import auth_required, admin_required


directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        try:
            all_directors = director_service.get_all()

            return directors_schema.dump(all_directors), 200

        except Exception as e:
            return str(e), 404

    @admin_required
    def post(self):
        try:
            req_json = request.json
            director_service.create(req_json)

        except Exception as e:
            return str(e), 404

        return "", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):

        try:
            director = director_service.get_one(did)

            if not director:
                return "Такого фильма нет в базе данных", 404

            return director_schema.dump(director), 200

        except Exception as e:
            return str(e), 404

    @admin_required
    def put(self, did):
        try:
            director = director_service.get_one(did)

            if not director:
                return "Такого фильма нет в базе данных", 404

            req_json = request.json
            req_json["id"] = did

            director_service.update(req_json)

            return "", 204

        except Exception as e:
            return str(e), 404

    @admin_required
    def delete(self, did):
        try:
            director = director_service.get_one(did)

            if not director:
                return "Такого фильма нет в базе данных", 404

            director_service.delete(did)

            return "", 204

        except Exception as e:
            return str(e), 404
