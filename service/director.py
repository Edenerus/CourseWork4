from dao.director import DirectorDao


class DirectorService:
    def __init__(self, dao: DirectorDao):
        self.dao = dao

    def get_one(self, did):
        return self.dao.get_one(did)

    def get_all(self, filter):
        return self.dao.get_all(filter)

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        did = data.get("id")
        director = self.get_one(did)

        fields_to_update = ["name"]

        for field in fields_to_update:
            setattr(director, field, data.get(field))

        self.dao.update(director)

    def delete(self, did):
        self.dao.delete(did)
