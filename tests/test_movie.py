from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

list_films = []

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)
    movie_1 = Movie(id=1,
               title='фильм 1',
               description="описание фильма 1",
               rating=10,
               director_id=1,
               genre_id=1,
               trailer="#",
               year=2015,
               genre="qrq",
               director="qrqy")

    movie_2 = Movie(id=2, title='фильм 2', description="описание фильма 2", genre_id=0)
    movie_3 = Movie(id=3, title='фильм 3', description="описание фильма 3", genre_id=0)
    movie_create = dict(id=3, title='фильм 3', description="описание фильма 3", genre_id=0)

    dict_film = {1: movie_1, 2: movie_2, 3: movie_3}

    global OBJECTS
    OBJECTS = [movie_1, movie_2, movie_3]


    movie_dao.get_one = MagicMock(side_effect=dict_film.get)
    movie_dao.get_all = MagicMock(return_value=[movie_2, movie_1, movie_3])
    movie_dao.update = MagicMock()
    movie_dao.create = MagicMock(return_value=Movie(**movie_create))
    movie_dao.delete = MagicMock()
    movie_dao.partially_update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        # assert movie is not None
        assert movie.id == 1



    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0
        # assert isinstance(movies, list)
        # assert movies == OBJECTS

    def test_create(self):
        movie_new = {'title': "test",
                     'description': "США после зе на отшибеовбой… И один из них - не тот, за кого себя выдает.",
                     }
        movie = self.movie_service.create(movie_new)
        assert movie.id > 0
        assert movie.title != ''

    def test_update(self):  # не работает
        movie_d = {
            'id': 3,
            'title': 'Superman'
        }
        self.movie_service.update(movie_d)

    def test_delete(self):
        del_movie = self.movie_service.delete(1)
        assert del_movie is None

    def test_partially_update(self):
        movie_d = {
            'id': 2,
            'title': 'восьмерка',
            'description': "США после зе на отшибеовбой… И один из них - не тот, за кого себя выдает.",
            'rating': 10,
            'director_id': 1,
            'genre_id': 0,
            'trailer': "#",
            'year': 2015,
            'genre': "qrq",
            'director': "qrqy"
        }
        self.movie_service.partially_update(movie_d)
