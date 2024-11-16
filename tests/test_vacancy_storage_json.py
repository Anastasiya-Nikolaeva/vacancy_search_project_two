from typing import Any, Dict, List


def test_add_vacancy_success(vacancy_storage: Any, mock_file_storage: Any) -> None:
    vacancy: Dict[str, str] = {"id": "1", "title": "Software Engineer"}
    mock_file_storage.return_value.read_data.return_value = []

    vacancy_storage.add_vacancy(vacancy)

    mock_file_storage.return_value.write_data.assert_called_once_with([vacancy])


def test_add_vacancy_duplicate(vacancy_storage: Any, mock_file_storage: Any, capsys: Any) -> None:
    vacancy: Dict[str, str] = {"id": "1", "title": "Software Engineer"}
    mock_file_storage.return_value.read_data.return_value = [vacancy]

    vacancy_storage.add_vacancy(vacancy)

    captured = capsys.readouterr()
    assert "Вакансия с id 1 уже существует." in captured.out

    mock_file_storage.return_value.write_data.assert_not_called()


def test_get_vacancies_no_criteria(vacancy_storage: Any, mock_file_storage: Any) -> None:
    vacancies: List[Dict[str, str]] = [
        {"id": "1", "title": "Software Engineer"},
        {"id": "2", "title": "Data Scientist"},
    ]
    mock_file_storage.return_value.read_data.return_value = vacancies

    result: List[Dict[str, str]] = vacancy_storage.get_vacancies()

    assert result == vacancies


def test_get_vacancies_with_criteria(vacancy_storage: Any, mock_file_storage: Any) -> None:
    vacancies: List[Dict[str, str]] = [
        {"id": "1", "title": "Software Engineer"},
        {"id": "2", "title": "Data Scientist"},
    ]
    mock_file_storage.return_value.read_data.return_value = vacancies

    result: List[Dict[str, str]] = vacancy_storage.get_vacancies(title="Data Scientist")

    assert result == [{"id": "2", "title": "Data Scientist"}]


def test_delete_vacancy_success(vacancy_storage: Any, mock_file_storage: Any) -> None:
    vacancy: Dict[str, str] = {"id": "1", "title": "Software Engineer"}
    mock_file_storage.return_value.read_data.return_value = [vacancy]

    vacancy_storage.delete_vacancy("1")

    mock_file_storage.return_value.delete_data.assert_called_once_with([vacancy])


def test_delete_vacancy_not_found(vacancy_storage: Any, mock_file_storage: Any) -> None:
    vacancy: Dict[str, str] = {"id": "1", "title": "Software Engineer"}
    mock_file_storage.return_value.read_data.return_value = [vacancy]

    vacancy_storage.delete_vacancy("2")

    mock_file_storage.return_value.delete_data.assert_not_called()
