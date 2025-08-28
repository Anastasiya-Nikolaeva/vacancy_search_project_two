from typing import Any, Dict

import pytest

from src.vacancy_api_handler import HeadHunter
from src.vacancy_storage_json import JSONVacancyStorage


@pytest.fixture
def mock_file_storage(mocker: Any) -> Any:
    """Создаем мок для JSONFileStorage."""
    return mocker.patch("src.file_utils.JSONFileStorage")


@pytest.fixture
def vacancy_storage(mock_file_storage: Any) -> JSONVacancyStorage:
    """Создаем экземпляр JSONVacancyStorage с мок-объектом."""
    storage = JSONVacancyStorage("test_vacancies.json")
    storage.file_storage = mock_file_storage.return_value
    return storage


@pytest.fixture
def mock_file_worker() -> Dict[str, Any]:
    """Создаем мок для file_worker."""
    return {}


@pytest.fixture
def headhunter(mock_file_worker: Dict[str, Any]) -> HeadHunter:
    """Создаем экземпляр HeadHunter с мок-объектом."""
    return HeadHunter(mock_file_worker)


@pytest.fixture
def temp_json_file(tmp_path: Any) -> Any:
    """Создаем временный JSON файл."""
    return tmp_path / "temp.json"
