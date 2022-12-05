from dao.model.movie import Movie
from dao.model.director import Director
from dao.model.genre import Genre


class MovieDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        entity = self.session.query(Movie).get(mid)

        return entity

    def get_all(self, filter):
        status = filter.get('status')
        page = filter.get('page')

        if status == 'new' and page is not None:
            return self.session.query(Movie).order_by(Movie.year.desc()).paginate(int(page), per_page=12).items
        elif page is not None:
            return self.session.query(Movie).paginate(int(page), per_page=12).items

        elif status is not None:
            return self.session.query(Movie).order_by(Movie.year.desc()).all()

        return self.session.query(Movie).all()

    def get_all_movies_director(self, director_id):
        all_movies = self.session.query(Movie).filter(Director.id == director_id).join(Director)

        return all_movies.all()

    def get_all_movies_genre(self, genre_id):
        all_movies = self.session.query(Movie).filter(Genre.id == genre_id).join(Genre)

        return all_movies.all()

    def get_all_movies_year(self, year):
        all_movies = self.session.query(Movie).filter(Movie.year == year)

        return all_movies.all()

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
