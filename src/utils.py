from typing import List

from src.vacancy_services import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам."""
    if not filter_words:
        return vacancies  # Если нет фильтров, возвращаем все вакансии

    filtered_vacancies = []
    for vac in vacancies:
        if isinstance(vac, Vacancy):  # Проверяем, что vac является экземпляром Vacancy
            if any(word.lower() in vac.title.lower() for word in filter_words) or any(
                word.lower() in vac.description.lower() for word in filter_words
            ):
                filtered_vacancies.append(vac)

    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Получает вакансии в заданном диапазоне зарплат."""
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
    except ValueError:
        print("Некорректный формат диапазона зарплат. Используйте формат 'число - число'.")
        return vacancies

    return [
        vac
        for vac in vacancies
        if isinstance(vac, Vacancy)  # Проверяем, что vac является экземпляром Vacancy
        and (vac.salary is not None and salary_from <= vac.salary <= salary_to)
    ]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате."""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получает топ N вакансий."""
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит вакансии на экран в понятном формате."""
    for vac in vacancies:
        print(f"Название: {vac.title}\nСсылка: {vac.url}\nЗарплата: {vac.salary}")
        if vac.description:  # Проверяем, есть ли описание
            print(f"Описание: {vac.description}")
        print()  # Печатаем пустую строку для разделения вакансий
