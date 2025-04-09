import json
import os
import pandas as pd
from src.utils import setup_logging
import logging
from dotenv import load_dotenv
import requests
from typing import Any

setup_logging()

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_events_data(df: pd.DataFrame) -> str:
    """
    Формирует JSON-ответ для страницы "События".
    Args:
        df: DataFrame с данными о транзакциях.
    Returns:
        JSON-строка с данными о событиях.
    """
    try:
        events = []
        for index, row in df.iterrows():
            event = {
                "date": str(row["Дата операции"]),  # Преобразование в строку для JSON
                "description": row["Описание"],
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
            }
            events.append(event)
        return json.dumps(
            events, ensure_ascii=False, indent=4
        )  # ensure_ascii=False для корректного отображения русских символов
    except Exception as e:
        logging.error(f"Ошибка при формировании JSON для событий: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)  # Возвращаем сообщение об ошибке в JSON


def get_cur_rate(currency: str) -> Any:
    """Функция получения курса валют."""
    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
        response.raise_for_status()  # Проверка на успешный статус ответа
        response_data = response.json()
        if "rates" in response_data and "RUB" in response_data["rates"]:
            return response_data["rates"]["RUB"]
        else:
            logging.error(f"Некорректный ответ от API для валюты {currency}: {response_data}")
            return None  # Или можно выбрасывать исключение, если нужно
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе курса валюты {currency}: {e}")
        return None  # Или можно выбрасывать исключение
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка при декодировании JSON ответа для валюты {currency}: {e}")
        return None
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при получении курса валюты {currency}: {e}")
        return None
