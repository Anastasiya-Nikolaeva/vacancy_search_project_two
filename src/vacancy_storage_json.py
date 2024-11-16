from abc import ABC, abstractmethod
from typing import Any

from src.file_utils import JSONFileStorage


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Any) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria: Any) -> Any:
        """Получает вакансии по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет вакансию из хранилища по идентификатору."""
        pass


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, filename: str = "vacancies.json") -> None:
        self._filename = filename  # Приватный атрибут
        self.file_storage = JSONFileStorage(self._filename)

    def add_vacancy(self, vacancy: Any) -> None:
        """Добавляет вакансию в JSON-файл."""
        if "id" not in vacancy:
            raise ValueError("Вакансия должна содержать уникальный идентификатор 'id'.")

        vacancies = self.file_storage.read_data()
        # Проверка на дублирование по уникальному идентификатору
        if any(vacancy.get("id") == v.get("id") for v in vacancies):
            print(f"Вакансия с id {vacancy['id']} уже существует.")
            return  # Не добавляем дубликаты
        vacancies.append(vacancy)
        self.file_storage.write_data(vacancies)

    def get_vacancies(self, **criteria: Any) -> Any:
        """Получает вакансии по указанным критериям."""
        vacancies = self.file_storage.read_data()
        # Фильтрация по критериям
        for key, value in criteria.items():
            vacancies = [vacancy for vacancy in vacancies if vacancy.get(key) == value]
        return vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет вакансию из JSON-файла по идентификатору."""
        vacancies = self.file_storage.read_data()
        vacancies_to_delete = [vacancy for vacancy in vacancies if vacancy.get("id") == vacancy_id]

        # Удаляем только если есть вакансии для удаления
        if vacancies_to_delete:
            self.file_storage.delete_data(vacancies_to_delete)
