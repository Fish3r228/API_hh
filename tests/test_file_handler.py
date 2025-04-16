import json
import pytest
from src.file_handler import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def json_saver(tmp_path):
    """Фикстура для тестирования JSONSaver"""
    filename = tmp_path / "test_vacancies.json"
    return JSONSaver(filename=filename)


def test_add_vacancy(json_saver):
    """Тест добавления вакансии"""
    vacancy = Vacancy("Python Dev", "link", {"from": 100000}, "desc")
    json_saver.add_vacancy(vacancy)

    with open(json_saver.filename, "r") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["title"] == "Python Dev"


def test_get_vacancies(json_saver):
    """Тест получения вакансий"""
    vacancy1 = Vacancy("Python Dev", "link1", {"from": 100000}, "Python experience")
    vacancy2 = Vacancy("Java Dev", "link2", {"from": 90000}, "Java experience")

    json_saver.add_vacancy(vacancy1)
    json_saver.add_vacancy(vacancy2)

    # Без фильтра
    all_vacancies = json_saver.get_vacancies()
    assert len(all_vacancies) == 2

    # С фильтром по ключевым словам
    filtered = json_saver.get_vacancies({"keywords": "Python"})
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Python Dev"


def test_delete_vacancy(json_saver):
    """Тест удаления вакансии"""
    vacancy = Vacancy("Python Dev", "link", {"from": 100000}, "desc")
    json_saver.add_vacancy(vacancy)

    # Проверяем, что вакансия добавлена
    assert len(json_saver.get_vacancies()) == 1

    # Удаляем вакансию
    json_saver.delete_vacancy(vacancy)

    # Проверяем, что вакансия удалена
    assert len(json_saver.get_vacancies()) == 0
