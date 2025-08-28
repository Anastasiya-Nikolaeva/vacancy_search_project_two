from typing import Any, Dict, List

import pytest


def test_connect_to_api_success(headhunter: Any, mocker: Any) -> None:
    # Мокаем requests.get для успешного ответа
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"items": []}

    response: Dict[str, Any] = headhunter._connect_to_api()

    assert response == {"items": []}
    mock_response.assert_called_once_with(headhunter._url, headers=headhunter._headers, params=headhunter._params)


def test_connect_to_api_failure(headhunter: Any, mocker: Any) -> None:
    # Мокаем requests.get для неуспешного ответа
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 404

    with pytest.raises(Exception) as excinfo:
        headhunter._connect_to_api()

    assert str(excinfo.value) == "Ошибка при подключении к API: 404"


def test_get_vacancies_success(headhunter: Any, mocker: Any) -> None:
    # Мокаем _connect_to_api для успешного ответа с одной вакансией
    mocker.patch.object(
        headhunter,
        "_connect_to_api",
        side_effect=[
            {"items": [{"id": "1", "name": "Software Engineer"}]},  # Первая страница
            {"items": []},  # Пустой ответ для завершения
        ],
    )

    vacancies: List[Dict[str, Any]] = headhunter.get_vacancies("Software")

    assert len(vacancies) == 1  # Ожидаем 1 вакансию
    assert vacancies[0]["id"] == "1"
    assert vacancies[0]["name"] == "Software Engineer"


def test_get_vacancies_no_results(headhunter: Any, mocker: Any) -> None:
    # Мокаем _connect_to_api для ответа без вакансий
    mocker.patch.object(headhunter, "_connect_to_api", return_value={"items": []})

    vacancies: List[Dict[str, Any]] = headhunter.get_vacancies("NonExistentKeyword")

    assert len(vacancies) == 0


def test_get_vacancies_multiple_pages(headhunter: Any, mocker: Any) -> None:
    # Мокаем _connect_to_api для нескольких страниц
    mocker.patch.object(
        headhunter,
        "_connect_to_api",
        side_effect=[
            {"items": [{"id": "1", "name": "Software Engineer"}]},
            {"items": [{"id": "2", "name": "Data Scientist"}]},
            {"items": []},  # Пустой ответ для завершения
        ],
    )

    vacancies: List[Dict[str, Any]] = headhunter.get_vacancies("Software")

    assert len(vacancies) == 2
    assert vacancies[0]["id"] == "1"
    assert vacancies[1]["id"] == "2"
