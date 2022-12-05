from flask import request
from flask_restx import Resource, Namespace

from helpers.container import auth_service
from helpers.container import user_service


auth_ns = Namespace("auth")


@auth_ns.route('/register/')
class RegisterViews(Resource):
    def post(self):
        try:
            req_json = request.json

            email = req_json.get("email")
            password = req_json.get("password")

            if None in [email, password]:
                return "", 401

            user_service.create(req_json)

        except Exception as e:
            return str(e), 404

        return "", 201


@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        try:
            req_json = request.json

            email = req_json.get("email", None)
            password = req_json.get("password", None)

            if None in [email, password]:
                return "", 401

            tokens = auth_service.generate_token(email, password)

        except Exception as e:
            return str(e), 404

        return tokens, 201

    def put(self):
        try:
            req_json = request.json

            access_token = req_json.get('access_token')
            refresh_token = req_json.get('refresh_token')

            valid = auth_service.valid_token(access_token, refresh_token)

            if not valid:
                return "Invalid token", 400

            tokens = auth_service.check_token(refresh_token)

        except Exception as e:
            return str(e), 404

        return tokens, 201
