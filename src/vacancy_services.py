from typing import Union


class Vacancy:
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: Union[float, int] = 0, description: str = "") -> None:
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary: Union[float, int]) -> float:
        """Валидирует значение зарплаты."""
        if salary is None or (isinstance(salary, (int, float)) and salary < 0):
            raise ValueError("Зарплата не может быть отрицательной.")
        return float(salary)

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary < other.salary

    def __le__(self, other: "Vacancy") -> bool:
        return self.salary <= other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        return self.salary > other.salary

    def __ge__(self, other: "Vacancy") -> bool:
        return self.salary >= other.salary

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __repr__(self) -> str:
        return (
            f"Vacancy(title='{self.title}', url='{self.url}', "
            f"salary={self.salary}, description='{self.description}')"
        )

    def __str__(self) -> str:
        return f"{self.title} - {self.salary} - {self.url}"
