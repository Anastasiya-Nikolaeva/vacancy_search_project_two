from typing import Any, Dict, List

from src.vacancy_api_handler import HeadHunter
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

    filter_words_input = input("Введите ключевые слова для фильтрации вакансий: ").strip()
    filter_words = filter_words_input.split() if filter_words_input else []

    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ").strip()

    # Получаем вакансии по запросу
    vacancies_list = headhunter.get_vacancies(search_query)

    # Фильтруем вакансии
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    # Получаем вакансии в заданном диапазоне зарплат
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Сортируем вакансии по зарплате
    sorted_vacancies = sort_vacancies(ranged_vacancies)

    # Получаем топ N вакансий
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Выводим вакансии
    print_vacancies(top_vacancies)


def filter_vacancies(vacancies: List[Dict[str, Any]], filter_words: List[str]) -> List[Dict[str, Any]]:
    """Фильтрует вакансии по ключевым словам."""
    if not filter_words:
        return vacancies  # Если нет фильтров, возвращаем все вакансии

    return [
        vac
        for vac in vacancies
        if isinstance(vac, dict)
        and (
            any(word.lower() in vac.get("name", "").lower() for word in filter_words)
            or any(word.lower() in vac.get("description", "").lower() for word in filter_words)
        )
    ]


def get_vacancies_by_salary(vacancies: List[Dict[str, Any]], salary_range: str) -> List[Dict[str, Any]]:
    """Получает вакансии в заданном диапазоне зарплат."""
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
    except ValueError:
        print("Некорректный формат диапазона зарплат.")
        return vacancies

    return [
        vac
        for vac in vacancies
        if isinstance(vac, dict)  # Проверяем, что vac является словарем
        and vac.get("salary")
        and (vac["salary"].get("from") is None or vac["salary"].get("from", 0) >= salary_from)
        and (vac["salary"].get("to") is None or vac["salary"].get("to", float("inf")) <= salary_to)
    ]


def sort_vacancies(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортирует вакансии по зарплате."""
    valid_vacancies = [vac for vac in vacancies if isinstance(vac, dict) and vac.get("salary")]
    return sorted(
        valid_vacancies,
        key=lambda x: (x["salary"].get("from") or 0),  # Если 'from' отсутствует, используем 0
        reverse=True,
    )


def get_top_vacancies(vacancies: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
    """Получает топ N вакансий."""
    return vacancies[:top_n] if top_n is not None else vacancies


def print_vacancies(vacancies: List[Dict[str, Any]]) -> None:
    """Выводит вакансии на экран."""
    if not vacancies:
        print("Нет вакансий для отображения.")
        return

    for vac in vacancies:
        title = vac.get("name", "Без названия")
        salary = vac.get("salary", {})
        salary_info = (
            f"{salary.get('from', 'не указана')} - {salary.get('to', 'не указана')} {salary.get('currency', '')}"
            if salary
            else "Зарплата не указана"
        )
        link = vac.get("alternate_url", "Ссылка недоступна")
        print(f"Название: {title}\nЗарплата: {salary_info}\nСсылка: {link}\n")


if __name__ == "__main__":
    # Здесь нужно передать экземпляр вашего класса для работы с файлами (работа с файлом или с сайтом)
    json_storage = JSONVacancyStorage("data/vacancies.json")
    user_interaction(json_storage)
