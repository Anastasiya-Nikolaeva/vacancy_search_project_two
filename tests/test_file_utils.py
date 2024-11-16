import json
from typing import Dict, List

from src.file_utils import JSONFileStorage  # Импортируйте ваш класс


def test_read_data(temp_json_file: str) -> None:
    # Записываем тестовые данные в файл
    test_data: List[Dict[str, str]] = [{"id": "1", "title": "Software Engineer"}]
    with open(temp_json_file, "w") as f:
        json.dump(test_data, f)

    storage: JSONFileStorage = JSONFileStorage(temp_json_file)
    result: List[Dict[str, str]] = storage.read_data()

    assert result == test_data


def test_write_data(temp_json_file: str) -> None:
    storage: JSONFileStorage = JSONFileStorage(temp_json_file)
    test_data: List[Dict[str, str]] = [{"id": "1", "title": "Software Engineer"}]

    storage.write_data(test_data)

    with open(temp_json_file, "r") as f:
        result: List[Dict[str, str]] = json.load(f)

    assert result == test_data


def test_delete_data(temp_json_file: str) -> None:
    storage: JSONFileStorage = JSONFileStorage(temp_json_file)
    initial_data: List[Dict[str, str]] = [
        {"id": "1", "title": "Software Engineer"},
        {"id": "2", "title": "Data Scientist"},
    ]
    storage.write_data(initial_data)

    # Удаляем вакансию с id '1'
    storage.delete_data([{"id": "1", "title": "Software Engineer"}])

    # Проверяем, что осталась только одна вакансия
    with open(temp_json_file, "r") as f:
        result: List[Dict[str, str]] = json.load(f)

    assert result == [{"id": "2", "title": "Data Scientist"}]


def test_delete_data_not_found(temp_json_file: str) -> None:
    storage: JSONFileStorage = JSONFileStorage(temp_json_file)
    initial_data: List[Dict[str, str]] = [{"id": "1", "title": "Software Engineer"}]
    storage.write_data(initial_data)

    # Пытаемся удалить вакансию, которая не существует
    storage.delete_data([{"id": "2", "title": "Data Scientist"}])

    # Проверяем, что данные остались прежними
    with open(temp_json_file, "r") as f:
        result: List[Dict[str, str]] = json.load(f)

    assert result == initial_data
