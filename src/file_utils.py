import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class FileStorage(ABC):
    @abstractmethod
    def read_data(self) -> List[Dict[str, Any]]:
        """Читает данные из файла."""
        pass

    @abstractmethod
    def write_data(self, data: List[Dict[str, Any]]) -> None:
        """Записывает данные в файл."""
        pass

    @abstractmethod
    def delete_data(self, data: List[Dict[str, Any]]) -> None:
        """Удаляет данные из файла."""
        pass


class JSONFileStorage(FileStorage):
    def __init__(self, filename: str = "./vacancies.json") -> None:
        self._filename = filename  # Приватный атрибут
        # Создаем файл, если он не существует
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f)  # Инициализируем пустым списком

    def read_data(self) -> Any:
        """Читает данные из JSON-файла."""
        try:
            with open(self._filename, "r", encoding="utf-8", errors="ignore") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Ошибка при чтении данных: {e}")
            return []  # Возвращаем пустой список в случае ошибки

    def write_data(self, data: List[Dict[str, Any]]) -> None:
        """Записывает данные в JSON-файл."""
        if not data:  # Проверяем, что данные не пустые
            return
        try:
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Ошибка при записи данных: {e}")

    def delete_data(self, data: List[Dict[str, Any]]) -> None:
        """Удаляет данные из JSON-файла."""
        current_data = self.read_data()
        # Удаляем элементы, которые есть в data
        current_data = [item for item in current_data if item not in data]
        self.write_data(current_data)
