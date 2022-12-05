from dao.model.director import Director


class DirectorDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        entity = self.session.query(Director).get(mid)

        return entity

    def get_all(self, filter):
        page = filter.get('page')

        if page is not None:
            return self.session.query(Director).paginate(int(page), per_page=12).items

        return self.session.query(Director).all()

    def create(self, data):
        director = Director(**data)

        self.session.add(director)
        self.session.commit()

        return director

    def update(self, director):
        self.session.add(director)
        self.session.commit()

        return director

    def delete(self, mid):
        director = self.get_one(mid)

        self.session.delete(director)
        self.session.commit()
