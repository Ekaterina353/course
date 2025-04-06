import pandas as pd
import json
from src.reports import calculate_category_spending  # Замените your_module на имя вашего файла


def test_calculate_category_spending():
    data = {
        "Дата операции": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05"],
        "Категория": ["Продукты", "Развлечения", "Продукты", "Транспорт"],
        "Сумма платежа": [100, 200, 150, 50],
    }
    df = pd.DataFrame(data)
    start_date_str = "2024-04-15"
    result = calculate_category_spending(df, "Продукты", start_date_str)
    result_dict = json.loads(result)
    assert result_dict["category"] == "Продукты"
    assert result_dict["start_date"] == start_date_str
    assert result_dict["total_spending"] == 250


def test_calculate_category_spending_no_data():
    data = {
        "Дата операции": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05"],
        "Категория": ["Продукты", "Развлечения", "Продукты", "Транспорт"],
        "Сумма платежа": [100, 200, 150, 50],
    }
    df = pd.DataFrame(data)
    start_date_str = "2024-04-15"
    result = calculate_category_spending(df, "Одежда", start_date_str)
    result_dict = json.loads(result)
    assert result_dict["category"] == "Одежда"
    assert result_dict["start_date"] == start_date_str
    assert result_dict["total_spending"] == 0


def test_calculate_category_spending_invalid_date():
    data = {"Дата операции": ["2024-01-15"], "Категория": ["Продукты"], "Сумма платежа": [100]}
    df = pd.DataFrame(data)
    start_date_str = "invalid-date"
    result = calculate_category_spending(df, "Продукты", start_date_str)
    result_dict = json.loads(result)
    assert "error" in result_dict
