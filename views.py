import json
import pandas as pd
from src.utils import setup_logging, parse_date
import logging
setup_logging()


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
                'date': str(row['Дата операции']),  # Преобразование в строку для JSON
                'description': row['Описание'],
                'amount': row['Сумма платежа'],
                'category': row['Категория']
            }
            events.append(event)
        return json.dumps(events, ensure_ascii=False,
                          indent=4)  # ensure_ascii=False для корректного отображения русских символов
    except Exception as e:
        logging.error(f"Ошибка при формировании JSON для событий: {e}")
        return json.dumps({'error': str(e)}, ensure_ascii=False)  # Возвращаем сообщение об ошибке в JSON
