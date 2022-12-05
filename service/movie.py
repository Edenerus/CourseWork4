from dao.movie import MovieDao


class MovieService:
    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, filters):

        if filters.get("director_id") is not None:
            movies = self.dao.get_all_movies_director(filters.get("director_id"))

        elif filters.get("genre_id") is not None:
            movies = self.dao.get_all_movies_genre(filters.get("genre_id"))

        elif filters.get("year") is not None:
            movies = self.dao.get_all_movies_year(filters.get("year"))

        else:
            movies = self.dao.get_all(filters)

        return movies

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)

        fields_to_update = ["title", "description", "trailer", "year", "rating", "genre_id", "director_id"]

        for field in fields_to_update:
            setattr(movie, field, data.get(field))

        self.dao.update(movie)

    def patch(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)

        fields_to_update = ["title", "description", "trailer", "year", "rating", "genre_id", "director_id"]

        for field in fields_to_update:
            if data.get(field):
                setattr(movie, field, data.get(field))

        self.dao.update(movie)

    def delete(self, mid):
        self.dao.delete(mid)
