from src.main import filter_vacancies, get_vacancies_by_salary
from src.vacancy import Vacancy


def test_filter_vacancies():
    """Тест фильтраций вакансий по ключевым словам"""
    vacancies = [
        Vacancy("Dev1", "link1", None, "Python experience required"),
        Vacancy("Dev2", "link2", None, "Java experience required"),
    ]

    filtered = filter_vacancies(vacancies, ["Python"])
    assert len(filtered) == 1
    assert filtered[0].title == "Dev1"

    filtered = filter_vacancies(vacancies, [])
    assert len(filtered) == 2


def test_get_vacancies_by_salary():
    """Тест фильтрации вакансий по зарплате"""
    vacancies = [
        Vacancy("Dev1", "link1", {"from": 100000, "to": 150000}, "desc1"),
        Vacancy("Dev2", "link2", {"from": 80000, "to": 120000}, "desc2"),
        Vacancy("Dev3", "link3", {"from": 150000, "to": 200000}, "desc3"),
    ]

    # Тест 1: Зарплата в диапазоне 90000-130000
    ranged = get_vacancies_by_salary(vacancies, "90000-130000")
    assert len(ranged) == 3
    assert ranged[0].title == "Dev1"
    assert ranged[1].title == "Dev2"

    # Тест 2: Без фильтра (None)
    ranged = get_vacancies_by_salary(vacancies, None)
    assert len(ranged) == 3

    # Тест 3: Неверный формат диапазона
    ranged = get_vacancies_by_salary(vacancies, "invalid-format")
    assert len(ranged) == 3

    # Тест 4: Граничные случаи
    ranged = get_vacancies_by_salary(vacancies, "100000-150000")
    assert len(ranged) == 3