from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from helpers.container import user_service
from helpers.decorators import auth_required, admin_required


users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        try:

            role = request.args.get('role')

            users = user_service.get_all(role)

            return users_schema.dump(users), 200

        except Exception as e:
            return str(e), 404


@users_ns.route('/password/')
class UpdatePasswordViews(Resource):
    def put(self):
        try:
            req_json = request.json

            email = req_json.get('email')
            old_password = req_json.get('password_1')
            new_password = req_json.get('password_2')

            user = user_service.get_one_by_email(email)

            if user_service.check_password(user.password, old_password):
                user.password = user_service.get_hash(new_password)
                result = UserSchema().dump(user)
                user_service.update(result)

            else:
                print("Password did not changed")

        except Exception as e:
            return str(e), 404

        return "", 201


@users_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        try:
            user = user_service.get_one(uid)

            if not user:
                return "Такого пользователя нет в базе данных", 404

            return user_schema.dump(user), 200

        except Exception as e:
            return str(e), 404

    @auth_required
    def patch(self, uid):
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

    @admin_required
    def delete(self, uid):
        try:
            user = user_service.get_one(uid)

            if not user:
                return "Такого пользователя нет в базе данных", 404

            user_service.delete(uid)

            return "", 204

        except Exception as e:
            return str(e), 404
