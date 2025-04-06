from src.services import find_profitable_categories
import json


def test_find_profitable_categories():
    transactions = [
        {"Дата операции": "2023-10-01", "Категория": "Супермаркеты", "Кешбэк": 100},
        {"Дата операции": "2023-10-05", "Категория": "Рестораны", "Кешбэк": 50},
        {"Дата операции": "2023-10-10", "Категория": "Супермаркеты", "Кешбэк": 150},
        {"Дата операции": "2023-11-01", "Категория": "Супермаркеты", "Кешбэк": 200},
    ]
    result = find_profitable_categories(2023, 10, transactions)
    expected = ["Супермаркеты"]  # Ожидаемый результат
    assert json.loads(result) == expected
