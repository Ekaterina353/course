import unittest
import pandas as pd
import json
from src.views import get_events_data


class TestGetEventsData(unittest.TestCase):

    def test_get_events_data_success(self):
        data = {
            "Дата операции": ["2024-01-01", "2024-01-02"],
            "Описание": ["Покупка в магазине", "Оплата интернета"],
            "Сумма платежа": [100.0, 500.0],
            "Категория": ["Продукты", "Интернет"],
        }
        df = pd.DataFrame(data)
        result = get_events_data(df)
        expected = json.dumps(
            [
                {"date": "2024-01-01", "description": "Покупка в магазине", "amount": 100.0, "category": "Продукты"},
                {"date": "2024-01-02", "description": "Оплата интернета", "amount": 500.0, "category": "Интернет"},
            ],
            ensure_ascii=False,
            indent=4,
        )
        self.assertEqual(result, expected)

    def test_get_events_data_empty_dataframe(self):
        df = pd.DataFrame()
        result = get_events_data(df)
        self.assertEqual(result, "[]")

    def test_get_events_data_exception(self):
        # Создаем DataFrame с некорректным типом данных, чтобы вызвать исключение
        data = {
            "Дата операции": ["2024-01-01"],
            "Описание": ["Покупка в магазине"],
            "Сумма платежа": ["invalid"],
            "Категория": ["Продукты"],
        }
        df = pd.DataFrame(data)
        result = get_events_data(df)
        self.assertTrue("error" in json.loads(result))


if __name__ == "__main__":
    unittest.main()
