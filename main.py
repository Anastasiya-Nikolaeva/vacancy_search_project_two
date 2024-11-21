from typing import Any

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy_api_handler import HeadHunter
from src.vacancy_services import Vacancy
from src.vacancy_storage_json import JSONVacancyStorage


def user_interaction(storage: Any) -> None:
    # Создаем экземпляр класса HeadHunter
    headhunter = HeadHunter(storage)

    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("Поисковой запрос не может быть пустым.")
        return

    top_n_input = input("Введите количество вакансий для вывода в топ N: ").strip()
    top_n = int(top_n_input) if top_n_input.isdigit() else 0

    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").strip()
    filter_words = filter_words_input.split() if filter_words_input else []

    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ").strip()

    # Получаем вакансии по запросу
    vacancies_list = headhunter.get_vacancies(search_query)

    if vacancies_list is None or not vacancies_list:
        print("Ошибка: Не удалось получить вакансии или список вакансий пуст.")
        return

    # Создаем экземпляры Vacancy
    vacancies = [
        Vacancy(
            title=vac.get("name", "Без названия"),
            url=vac.get("alternate_url", ""),
            salary=vac.get("salary", {}).get("from", 0) if vac.get("salary") is not None else 0,
            description=vac.get("description", ""),
        )
        for vac in vacancies_list
        if isinstance(vac, dict)
    ]

    # Фильтруем вакансии
    filtered_vacancies = filter_vacancies(vacancies, filter_words)

    # Получаем вакансии в заданном диапазоне зарплат
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Сортируем вакансии по зарплате
    sorted_vacancies = sort_vacancies(ranged_vacancies)

    # Получаем топ N вакансий
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Выводим вакансии
    if top_vacancies:
        print("Топ вакансий:")
        print_vacancies(top_vacancies)
        storage.save([vac.to_dict() for vac in top_vacancies])  # Сохраняем вакансии в формате словарей
        print("Вакансии успешно сохранены в файл.")
    else:
        print("Нет вакансий для отображения.")


if __name__ == "__main__":
    try:
        # Создаем экземпляр класса для работы с файлами
        json_storage = JSONVacancyStorage("data/vacancies.json")
        user_interaction(json_storage)
    except FileNotFoundError:
        print("Ошибка: Файл 'vacancies.json' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
