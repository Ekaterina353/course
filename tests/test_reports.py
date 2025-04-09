import pandas as pd
import json
import pytest
from src.reports import calculate_category_spending  # Замените your_module на имя вашего файла


@pytest.fixture
def sample_dataframe():
    data = {
        "Дата операции": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05"],
        "Категория": ["Продукты", "Развлечения", "Продукты", "Транспорт"],
        "Сумма платежа": [100, 200, 150, 50],
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "category, start_date_str, expected_spending, expected_error",
    [
        ("Продукты", "2024-04-15", 250, None),  # Базовый случай
        ("Одежда", "2024-04-15", 0, None),  # Нет данных для категории
        ("Продукты", "2024-03-01", 250, None), # Дата раньше всех транзакций
        ("Транспорт", "2024-04-01", 50, None),  # Одна транзакция в категории
        ("Развлечения", "2024-01-01", 200, None),# Несколько транзакций, дата в начале
        ("Продукты", "invalid-date", None, "error"),  # Некорректная дата
    ],
)
def test_calculate_category_spending(sample_dataframe, category, start_date_str, expected_spending, expected_error):
    """
    Тестирует функцию calculate_category_spending с использованием фикстуры и параметризации.
    """
    result = calculate_category_spending(sample_dataframe, category, start_date_str)
    result_dict = json.loads(result)

    assert result_dict["category"] == category
    assert result_dict["start_date"] == start_date_str

    if expected_error:
        assert "error" in result_dict
    else:
        assert result_dict["total_spending"] == expected_spending
