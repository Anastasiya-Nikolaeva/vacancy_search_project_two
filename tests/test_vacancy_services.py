from src.vacancy_services import Vacancy


def test_vacancy_initialization() -> None:
    vacancy: Vacancy = Vacancy(
        title="Software Engineer", url="http://example.com", salary=100000, description="Develop software."
    )

    assert vacancy.title == "Software Engineer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == 100000
    assert vacancy.description == "Develop software."


def test_validate_salary_with_negative() -> None:
    vacancy: Vacancy = Vacancy(
        title="Software Engineer", url="http://example.com", salary=-50000, description="Develop software."
    )

    assert vacancy.salary == 0  # Проверяем, что отрицательная зарплата валидируется в 0


def test_compare_vacancies() -> None:
    vacancy1: Vacancy = Vacancy(
        title="Junior Developer", url="http://example.com/junior", salary=50000, description="Junior position."
    )
    vacancy2: Vacancy = Vacancy(
        title="Senior Developer", url="http://example.com/senior", salary=100000, description="Senior position."
    )

    assert vacancy1 < vacancy2
    assert vacancy1 <= vacancy2
    assert vacancy2 > vacancy1
    assert vacancy2 >= vacancy1
    assert vacancy1 != vacancy2


def test_vacancy_repr() -> None:
    vacancy: Vacancy = Vacancy(
        title="Software Engineer", url="http://example.com", salary=100000.0, description="Develop software."
    )

    expected_repr: str = (
        "Vacancy(title='Software Engineer', "
        "url='http://example.com', "
        "salary=100000.0, "
        "description='Develop software.')"
    )
    assert repr(vacancy) == expected_repr
