from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class Parser(ABC):
    def __init__(self, file_worker: Any) -> None:
        self._file_worker = file_worker

    @abstractmethod
    def _connect_to_api(self) -> Dict[str, Any]:
        """Подключается к API и возвращает ответ"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии по заданному ключевому слову"""
        pass


class HeadHunter(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self, file_worker: Any) -> None:
        super().__init__(file_worker)
        self._url: str = "https://api.hh.ru/vacancies"
        self._headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self._params: Dict[str, Any] = {"text": "", "per_page": 100, "page": 0}
        self._vacancies: List[Dict[str, Any]] = []

    def _connect_to_api(self) -> Dict[str, Any]:
        """Подключается к API hh.ru и проверяет статус-код ответа"""
        response = requests.get(self._url, headers=self._headers, params=self._params)
        if response.status_code != 200:
            raise Exception(f"Ошибка при подключении к API: {response.status_code}")
        return response.json()

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии по заданному ключевому слову."""
        self._params["text"] = keyword
        self._vacancies = []  # Очищаем список перед загрузкой
        seen_ids = set()  # Множество для хранения уникальных идентификаторов вакансий

        for page in range(20):  # Ограничиваем количество страниц
            self._params["page"] = page
            data = self._connect_to_api()  # Подключаемся к API
            items = data.get("items", [])

            for item in items:
                if item["id"] not in seen_ids:  # Проверяем, не добавляли ли мы уже эту вакансию
                    seen_ids.add(item["id"])  # Добавляем идентификатор в множество
                    self._vacancies.append(item)  # Собираем данные из ключа 'items'

            if not items:  # Если нет больше вакансий, выходим из цикла
                break

        return self._vacancies  # Возвращаем собранные вакансии
