class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title: str, link: str, salary: dict or str, description: str):
        self.title = title
        self.link = link
        self.salary = self.validate_salary(salary)
        self.description = description

    def validate_salary(self, salary):
        """Валидация данных о зарплатах"""
        if isinstance(salary, str):
            return {"from": 0, "to": 0, "currency": salary}

        if not salary:
            return {"from": 0, "to": 0, "currency": "Зарплата не указана"}

        salary_from = salary.get("from") if salary.get("from") else 0
        salary_to = salary.get("to") if salary.get("to") else 0
        currency = salary.get("currency") if salary.get("currency") else "RUR"

        return {"from": salary_from, "to": salary_to, "currency": currency}

    @property
    def avg_salary(self):
        """Средняя зарплата"""
        if self.salary["from"] and self.salary["to"]:
            return (self.salary["from"] + self.salary["to"]) / 2
        elif self.salary["from"]:
            return self.salary["from"]
        elif self.salary["to"]:
            return self.salary["to"]
        else:
            return 0

    def __str__(self):
        salary_info = f"от {self.salary['from']}" if self.salary["from"] else ""
        if self.salary["to"]:
            salary_info += (
                f" до {self.salary['to']}" if salary_info else f"до {self.salary['to']}"
            )
        if not salary_info:
            salary_info = "Зарплата не указана"
        else:
            salary_info += f" {self.salary['currency']}"

        return (
            f"{self.title}\n{salary_info}\n{self.description[:100]}...\n{self.link}\n"
        )

    def __lt__(self, other):
        return self.avg_salary < other.avg_salary

    def __le__(self, other):
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other):
        return self.avg_salary > other.avg_salary

    def __ge__(self, other):
        return self.avg_salary >= other.avg_salary

    def to_dict(self):
        """Преобразование вакансии в словарь"""
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def cast_to_object_list(cls, vacancies_data):
        """Преобразование набора данных из JSON в список объектов"""
        vacancies = []
        for vacancy in vacancies_data:
            title = vacancy.get("name", "Название не указано")
            link = vacancy.get("alternate_url", "Ссылка не указана")
            salary = vacancy.get("salary")
            description = vacancy.get("snippet", {}).get(
                "requirement", "Описание не указано"
            )

            vacancies.append(cls(title, link, salary, description))
        return vacancies
