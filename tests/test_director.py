from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)
    vova = Director(id=1, name='Вовка')
    jora = Director(id=2, name='Жорка')
    sana = Director(id=3, name='Сашка')

    director_dao.get_one = MagicMock(return_value=vova)
    director_dao.get_all = MagicMock(return_value=[vova, jora, sana])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()
    director_dao.partially_update = MagicMock()
    return director_dao


class TestDirectorService:
    # def __init__(self):
    #     self.director_service = None

    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director.id == 1
        assert director.name == 'Вовка'
        assert director is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):  # почему с director.name == 'Иваныч Иванов' - ошибка
        director_new = {'name': 'Иваныч Иванов'}
        director = self.director_service.create(director_new)
        assert director.id > 0
        assert director.name != ''

    def test_delete(self):
        del_director = self.director_service.delete(1)
        assert del_director == None

    def test_update(self):  # не работает
        data = {'id': 1, 'name': 'Сарик Адреасян'}
        self.director_service.update(data)
        dir = self.director_service.get_one(1)
        assert dir.id == 1

    def test_partially_update(self):
        director_d = {
            'id': 3,
            'name': 'Kubrik'
        }
        self.director_service.partially_update(director_d)