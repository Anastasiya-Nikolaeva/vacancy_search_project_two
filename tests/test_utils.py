from typing import List

import pytest

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy_services import Vacancy


def test_filter_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy("Software Engineer", "Develop software", 1000, "http://example.com/1"),
        Vacancy("Data Scientist", "Analyze data", 1200, "http://example.com/2"),
        Vacancy("Web Developer", "Build websites", 900, "http://example.com/3"),
    ]

    # Тест без фильтров
    assert filter_vacancies(vacancies, []) == vacancies

    # Тест с фильтром по заголовку
    assert len(filter_vacancies(vacancies, ["Software"])) == 1
    assert filter_vacancies(vacancies, ["Engineer"])[0].title == "Software Engineer"

    # Тест с фильтром по описанию
    assert len(filter_vacancies(vacancies, ["data"])) == 1
    assert filter_vacancies(vacancies, ["data"])[0].title == "Data Scientist"

    # Тест с фильтром, который не находит совпадений
    assert filter_vacancies(vacancies, ["Manager"]) == []


def test_get_vacancies_by_salary() -> None:
    vacancies: List[Vacancy] = [
        Vacancy("Software Engineer", "Develop software", 1000, "http://example.com/1"),
        Vacancy("Data Scientist", "Analyze data", 1200, "http://example.com/2"),
        Vacancy("Web Developer", "Build websites", 900, "http://example.com/3"),
    ]

    # Тест без диапазона
    assert get_vacancies_by_salary(vacancies, "") == vacancies

    # Тест с корректным диапазоном
    assert len(get_vacancies_by_salary(vacancies, "900-1100")) == 2

    # Тест с некорректным диапазоном
    assert get_vacancies_by_salary(vacancies, "abc-def") == vacancies


def test_sort_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy("Software Engineer", "Develop software", 1000, "http://example.com/1"),
        Vacancy("Data Scientist", "Analyze data", 1200, "http://example.com/2"),
        Vacancy("Web Developer", "Build websites", 900, "http://example.com/3"),
    ]

    sorted_vacancies: List[Vacancy] = sort_vacancies(vacancies)
    assert sorted_vacancies[0].title == "Data Scientist"
    assert sorted_vacancies[1].title == "Software Engineer"
    assert sorted_vacancies[2].title == "Web Developer"


def test_get_top_vacancies() -> None:
    vacancies: List[Vacancy] = [
        Vacancy("Software Engineer", "Develop software", 1000, "http://example.com/1"),
        Vacancy("Data Scientist", "Analyze data", 1200, "http://example.com/2"),
        Vacancy("Web Developer", "Build websites", 900, "http://example.com/3"),
    ]

    top_vacancies: List[Vacancy] = get_top_vacancies(vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].title == "Software Engineer"
    assert top_vacancies[1].title == "Data Scientist"

    # Тест с нулевым значением
    assert get_top_vacancies(vacancies, 0) == vacancies


def test_print_vacancies(capfd: pytest.CaptureFixture) -> None:
    vacancies: List[Vacancy] = [
        Vacancy("Software Engineer", "http://example.com/1", 1000, "Develop software"),
        Vacancy("Data Scientist", "http://example.com/2", 1200, "Analyze data"),
    ]

    print_vacancies(vacancies)

    captured = capfd.readouterr()  # Захватываем вывод

    # Проверяем, что вывод содержит ожидаемые строки
    assert "Название: Software Engineer" in captured.out
    assert "Ссылка: http://example.com/1" in captured.out
    assert "Зарплата: 1000.0" in captured.out  # Обратите внимание на .0, так как salary приводится к float
    assert "Описание: Develop software" in captured.out
    assert "" in captured.out  # Проверяем, что есть пустая строка между вак
