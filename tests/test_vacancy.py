from src.vacancy import Vacancy


def test_vacancy_creation():
    """Тест создания вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        link="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Требуется опыт работы с Python",
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.link == "https://hh.ru/vacancy/123"
    assert vacancy.salary["from"] == 100000
    assert vacancy.salary["to"] == 150000
    assert vacancy.description == "Требуется опыт работы с Python"


def test_vacancy_comparison():
    """Тест сравнения вакансий по зарплате"""
    vacancy1 = Vacancy("Dev1", "link1", {"from": 100000}, "desc1")
    vacancy2 = Vacancy("Dev2", "link2", {"from": 150000}, "desc2")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 != vacancy2


def test_avg_salary():
    """Тест расчета средней зарплаты"""
    vacancy1 = Vacancy("Dev1", "link1", {"from": 100000, "to": 150000}, "desc1")
    vacancy2 = Vacancy("Dev2", "link2", {"from": 120000}, "desc2")
    vacancy3 = Vacancy("Dev3", "link3", {"to": 130000}, "desc3")
    vacancy4 = Vacancy("Dev4", "link4", None, "desc4")

    assert vacancy1.avg_salary == 125000
    assert vacancy2.avg_salary == 120000
    assert vacancy3.avg_salary == 130000
    assert vacancy4.avg_salary == 0


def test_cast_to_object_list():
    """Тест преобразования данных в объекты Vacancy"""
    data = [
        {
            "name": "Python Dev",
            "alternate_url": "https://hh.ru/123",
            "salary": {"from": 100000},
            "snippet": {"requirement": "Опыт работы"},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(data)

    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Dev"
