from src.api import HeadHunterAPI
from unittest.mock import patch, Mock


@patch("requests.get")
def test_get_vacancies_success(mock_get):
    """Тест успешного получения вакансий"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"name": "Python Developer"}]}
    mock_get.return_value = mock_response

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"