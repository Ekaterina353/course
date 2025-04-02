import json
import logging
from datetime import datetime
from typing import List, Dict


def find_profitable_categories(year: int, month: int, transactions: List[Dict]) -> str:
    """
    Определяет выгодные категории повышенного кэшбэка за указанный месяц.
    Args:
        year: Год для расчета.
        month: Месяц для расчета.
        transactions: Список словарей с данными о транзакциях.
    Returns:
        JSON-строка с выгодными категориями.
    """
    try:
        #  Реализация логики определения выгодных категорий
        #  Пример:
        category_totals = {}
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')  # Или другой формат
            if transaction_date.year == year and transaction_date.month == month:
                category = transaction['Категория']
                cashback = transaction['Кешбэк']
                if category in category_totals:
                    category_totals[category] += cashback
                else:
                    category_totals[category] = cashback
        #  Найти категории с максимальным кэшбэком
        if category_totals:
            best_categories = [category for category, total in category_totals.items() if
                               total == max(category_totals.values())]
        else:
            best_categories = []
        return json.dumps(best_categories, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при определении выгодных категорий: {e}")
        return json.dumps({'error': str(e)}, ensure_ascii=False)
