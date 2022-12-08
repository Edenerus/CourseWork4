from contextlib import suppress
from typing import Any, Dict, List, Type

from sqlalchemy.exc import IntegrityError

from config import Config
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.model.director import Director
from server import create_app
from db_setup import db, models
from utils import read_json


def load_data(data: List[Dict[str, Any]], model: Type[models.Base]) -> None:
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))


if __name__ == '__main__':
    fixtures: Dict[str, List[Dict[str, Any]]] = read_json("fixtures.json")

    app_config = Config()
    app1 = create_app(app_config)

    with app1.app_context():
        # TODO: [fixtures] Добавить модели Directors и Movies
        load_data(fixtures['genres'], Genre)
        load_data(fixtures['movies'], Movie)
        load_data(fixtures['directors'], Director)

        with suppress(IntegrityError):
            db.session.commit()

