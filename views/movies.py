from flask import request
from flask_restx import Resource, Namespace

from helpers.container import movie_service
from dao.model.movie import MovieSchema
from helpers.decorators import auth_required, admin_required


movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        try:

            director = request.args.get('director_id')
            genre = request.args.get('genre_id')
            year = request.args.get('year')
            status = request.args.get('status')
            page = request.args.get('page')

            filters = {
                "director_id": director,
                "genre_id": genre,
                "year": year,
                'status': status,
                'page': page
            }

            movies = movie_service.get_all(filters)

            return movies_schema.dump(movies), 200

        except Exception as e:
            return str(e), 404

    @admin_required
    def post(self):
        try:
            req_json = request.json
            movie_service.create(req_json)

        except Exception as e:
            return str(e), 404

        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)

            if not movie:
                return "Такого фильма нет в базе данных", 404

            return movie_schema.dump(movie), 200

        except Exception as e:
            return str(e), 404

    @admin_required
    def put(self, mid):
        try:

            req_json = request.json
            req_json["id"] = mid

            movie = movie_service.get_one(mid)

            if not movie:
                return "Такого фильма нет в базе данных", 404

            movie_service.update(req_json)

            return "", 204

        except Exception as e:
            return str(e), 404

    @admin_required
    def patch(self, mid):
        try:

            req_json = request.json
            req_json["id"] = mid

            movie = movie_service.get_one(mid)

            if not movie:
                return "Такого фильма нет в базе данных", 404

            movie_service.patch(req_json)

            return "", 204

        except Exception as e:
            return str(e), 404

    @admin_required
    def delete(self, mid):
        try:
            movie = movie_service.get_one(mid)

            if not movie:
                return "Такого фильма нет в базе данных", 404

            movie_service.delete(mid)

            return "", 204

        except Exception as e:
            return str(e), 404
