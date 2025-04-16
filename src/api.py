import requests
from src.abstract_classes import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "area": 113,  # 113 — Россия
        }

    def get_vacancies(self, search_query: str) -> list[dict]:
        """Получение вакансий по поисковому запросу"""
        self.params["text"] = search_query

        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=10  # Добавляем таймаут
            )
            response.raise_for_status()  # Проверка на HTTP-ошибки
            return response.json().get("items", [])

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к API HH: {e}")
