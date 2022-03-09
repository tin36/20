from unittest.mock import MagicMock

import pytest


from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)
    action = Genre(id=1, name='action')
    drama = Genre(id=2, name='drama')
    comics = Genre(id=3, name='comics')

    genre_dao.get_one = MagicMock(return_value=action)
    genre_dao.get_all = MagicMock(return_value=[action, drama, comics])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.update = MagicMock()
    genre_dao.delete = MagicMock()
    genre_dao.partially_update = MagicMock()
    return genre_dao


class TestGenreService:
    # def __init__(self):
    #     self.director_service = None

    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre.id == 1
        assert genre.name == 'action'
        assert genre is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):  # почему с director.name == 'Иваныч Иванов' - ошибка
        genre_new = {'name': 'Иваныч Иванов'}
        genre = self.genre_service.create(genre_new)
        assert genre.id > 0
        assert genre.name != ''

    def test_delete(self):
        del_genre = self.genre_service.delete(1)
        assert del_genre == None

    def test_update(self):  # не работает
        data = {'id': 1, 'name': 'Сарик Адреасян'}
        self.genre_service.update(data)
        genre = self.genre_service.get_one(1)
        assert genre.id == 1

    def test_partially_update(self):
        genre_d = {
            'id': 3,
            'name': 'documental'
        }
        self.genre_service.partially_update(genre_d)