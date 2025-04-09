import pandas as pd
import json
import pytest
from src.views import get_events_data


@pytest.fixture
def sample_dataframe():
    """Фикстура для создания DataFrame с тестовыми данными."""
    data = {
        "Дата операции": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Описание": ["Покупка в магазине", "Оплата интернета", "Пополнение счета"],
        "Сумма платежа": [100.0, 500.0, 200.0],
        "Категория": ["Продукты", "Интернет", "Разное"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_dataframe():
    """Фикстура для создания пустого DataFrame."""
    return pd.DataFrame()


@pytest.fixture
def invalid_dataframe():
    """Фикстура для создания DataFrame с некорректными данными."""
    data = {
        "Дата операции": ["2024-01-01"],
        "Описание": ["Покупка в магазине"],
        "Сумма платежа": ["invalid"],
        "Категория": ["Продукты"],
    }
    return pd.DataFrame(data)


def expected_json(data):
    """Вспомогательная функция для создания ожидаемого JSON."""
    return json.dumps(data, ensure_ascii=False, indent=4)


class TestGetEventsData:

    @pytest.mark.parametrize(  # Параметризация для разных входных данных
        "data, expected",
        [
            (
                    {
                        "Дата операции": ["2024-01-01", "2024-01-02"],
                        "Описание": ["Покупка в магазине", "Оплата интернета"],
                        "Сумма платежа": [100.0, 500.0],
                        "Категория": ["Продукты", "Интернет"],
                    },
                    [
                        {
                            "date": "2024-01-01",
                            "description": "Покупка в магазине",
                            "amount": 100.0,
                            "category": "Продукты",
                        },
                        {
                            "date": "2024-01-02",
                            "description": "Оплата интернета",
                            "amount": 500.0,
                            "category": "Интернет",
                        },
                    ],
            ),
            (
                    {
                        "Дата операции": ["2024-02-15"],
                        "Описание": ["Зарплата"],
                        "Сумма платежа": [50000.0],
                        "Категория": ["Доход"],
                    },
                    [
                        {
                            "date": "2024-02-15",
                            "description": "Зарплата",
                            "amount": 50000.0,
                            "category": "Доход",
                        }
                    ],
            ),
        ],
    )
    def test_get_events_data_success(self, data, expected):
        """Тест для успешной обработки DataFrame."""
        df = pd.DataFrame(data)
        result = get_events_data(df)
        assert result == expected_json(expected)

    def test_get_events_data_empty_dataframe(self, empty_dataframe):
        """Тест для обработки пустого DataFrame."""
        result = get_events_data(empty_dataframe)
        assert result == "[]"  # Используем assert вместо self.assertEqual

    def test_get_events_data_exception(self, invalid_dataframe):
        """Тест для проверки обработки исключения."""
        result = get_events_data(invalid_dataframe)
        assert "error" in json.loads(result)
