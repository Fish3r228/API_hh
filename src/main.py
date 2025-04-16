from src.api import HeadHunterAPI
from src.file_handler import JSONSaver
from src.vacancy import Vacancy


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать в программу для работы с вакансиями!")

    # Получение вакансий с hh.ru
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос (например, Python): ")

    try:
        hh_vacancies = hh_api.get_vacancies(search_query)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
        print(f"\nНайдено {len(vacancies_list)} вакансий по запросу '{search_query}'")
    except Exception as e:
        print(f"Ошибка при получении вакансий: {e}")
        return

    # Сохранение вакансий в файл
    json_saver = JSONSaver()
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)
    print(f"Вакансии сохранены в файл {json_saver.filename}")

    # Фильтрация и сортировка вакансий
    top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
    filter_words = input(
        "Введите ключевые слова для фильтрации вакансий (через пробел): "
    ).split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ")

    # Применение фильтров
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Сортировка и вывод результатов
    sorted_vacancies = sorted(ranged_vacancies, reverse=True)
    top_vacancies = sorted_vacancies[:top_n] if top_n else sorted_vacancies

    print("\nРезультаты поиска:")
    for i, vacancy in enumerate(top_vacancies, 1):
        print(f"\nВакансия #{i}")
        print(vacancy)

    # Дополнительные операции с файлом
    while True:
        action = input("\nХотите выполнить дополнительные действия? (да/нет): ").lower()
        if action != "да":
            break

        print("\nДоступные действия:")
        print("1. Показать все вакансии из файла")
        print("2. Фильтровать вакансии по ключевым словам")
        print("3. Удалить вакансию")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            all_vacancies = json_saver.get_vacancies()
            for i, vacancy in enumerate(all_vacancies, 1):
                print(f"\nВакансия #{i}")
                print(Vacancy(**vacancy))

        elif choice == "2":
            keywords = input("Введите ключевые слова для поиска: ").split()
            filtered = json_saver.get_vacancies({"keywords": " ".join(keywords)})
            for i, vacancy in enumerate(filtered, 1):
                print(f"\nВакансия #{i}")
                print(Vacancy(**vacancy))

        elif choice == "3":
            title = input("Введите название вакансии для удаления: ")
            all_vacancies = json_saver.get_vacancies()
            found = [
                Vacancy(**v)
                for v in all_vacancies
                if title.lower() in v["title"].lower()
            ]

            if not found:
                print("Вакансии не найдены")
                continue

            for i, vacancy in enumerate(found, 1):
                print(f"\nВакансия #{i}")
                print(vacancy)

            to_delete = int(input("Введите номер вакансии для удаления: ")) - 1
            if 0 <= to_delete < len(found):
                json_saver.delete_vacancy(found[to_delete])
                print("Вакансия удалена")
            else:
                print("Неверный номер")

        elif choice == "4":
            break

        else:
            print("Неверный выбор")


def filter_vacancies(vacancies, filter_words):
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description = vacancy.description.lower()
        if any(word.lower() in description for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies, salary_range):
    """Фильтрация вакансий по диапазону зарплаты"""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        print("Неверный формат диапазона зарплат")
        return vacancies

    ranged = []
    for vacancy in vacancies:
        # Проверяем, что зарплата "от" >= минимальной И зарплата "до" <= максимальной
        # ИЛИ что зарплата попадает в диапазон хотя бы одной границей
        if (vacancy.salary["from"] is not None and vacancy.salary["from"] >= min_salary) or \
                (vacancy.salary["to"] is not None and vacancy.salary["to"] <= max_salary):
            ranged.append(vacancy)

    return ranged


if __name__ == "__main__":
    user_interaction()
