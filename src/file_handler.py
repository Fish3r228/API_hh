import json

from src.abstract_classes import FileHandler


class JSONSaver(FileHandler):
    """Класс для сохранения вакансий в JSON-файле"""

    def __init__(self, filename="vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy):
        """Добавление вакансии в файл"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(vacancy.to_dict())

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_vacancies(self, criteria: dict = None):
        """Получение вакансий из файла по критериям"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        if not criteria:
            return data

        filtered_vacancies = []
        for vacancy in data:
            match = True
            for key, value in criteria.items():
                if key == "salary_from" and vacancy["salary"]["from"] < value:
                    match = False
                elif key == "salary_to" and vacancy["salary"]["to"] > value:
                    match = False
                elif (
                    key == "keywords"
                    and value.lower() not in vacancy["description"].lower()
                ):
                    match = False
                elif key in vacancy and value.lower() not in vacancy[key].lower():
                    match = False

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy):
        """Удаление вакансии из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        vacancy_dict = vacancy.to_dict()
        data = [v for v in data if v != vacancy_dict]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
