import json
import pandas as pd
from datetime import datetime, timedelta
import logging

def calculate_category_spending(df: pd.DataFrame, category: str, start_date_str: str) -> str:
    """
    Рассчитывает траты по указанной категории за последние три месяца.
    Args:
        df: DataFrame с данными о транзакциях.
        category: Категория для расчета.
        start_date_str: Дата отсчета трехмесячного периода (в формате YYYY-MM-DD).
    Returns:
        JSON-строка с данными о тратах.
    """
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = start_date - timedelta(days=90)
        # Фильтрация данных
        filtered_df = df[
            (df['Категория'] == category) &
            (pd.to_datetime(df['Дата операции']) >= end_date) &
            (pd.to_datetime(df['Дата операции']) <= start_date)
        ]
        total_spending = filtered_df['Сумма платежа'].sum()
        result = {
            'category': category,
            'start_date': start_date_str,
            'total_spending': total_spending
        }
        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при расчете трат по категории: {e}")
        return json.dumps({'error': str(e)}, ensure_ascii=False)
