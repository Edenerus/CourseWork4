from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from helpers.container import user_service


users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        try:

            role = request.args.get('role')

            users = user_service.get_all(role)

            return users_schema.dump(users), 200

        except Exception as e:
            return str(e), 404

    def post(self):
        try:
            req_json = request.json
            user_service.create(req_json)

        except Exception as e:
            return str(e), 404

        return "", 201


@users_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        try:
            user = user_service.get_one(uid)

            if not user:
                return "Такого пользователя нет в базе данных", 404

            return user_schema.dump(user), 200

        except Exception as e:
            return str(e), 404

    def put(self, uid):
        try:

            req_json = request.json
            req_json["id"] = uid

            user = user_service.get_one(uid)

            if not user:
                return "Такого пользователя нет в базе данных", 404

            user_service.update(req_json)

            return "", 204

        except Exception as e:
            return str(e), 404

    def delete(self, uid):
        try:
            user = user_service.get_one(uid)

            if not user:
                return "Такого пользователя нет в базе данных", 404

            user_service.delete(uid)

            return "", 204

        except Exception as e:
            return str(e), 404
