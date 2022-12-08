from config import Config
from server import create_app
from db_setup import db

if __name__ == '__main__':
    with create_app(Config).app_context():
        db.drop_all()
        db.create_all()
