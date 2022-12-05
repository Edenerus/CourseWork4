from flask import Flask
from flask_restx import Api

from db_setup import db
from views.genres import genres_ns
from views.auth import auth_ns
from views.directors import directors_ns
from views.movies import movies_ns
from views.users import users_ns


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)
    api = Api(app)

    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(users_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(auth_ns)

    return app
