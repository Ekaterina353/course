import logging
from src.utils import setup_logging, read_excel
from src.views import get_events_data
from src.services import find_profitable_categories
from src.reports import calculate_category_spending
setup_logging()


def main():
    """Основная функция приложения."""

    file_path = 'data/operations.xlsx'
    df = read_excel(file_path)

    if df is not None:
        # Пример использования функций
        events_json = get_events_data(df)
        print("События:", events_json)
        transactions = df.to_dict('records')
        profitable_categories_json = find_profitable_categories(2023, 10, transactions)
        print("Выгодные категории:", profitable_categories_json)
        category_spending_json = calculate_category_spending(df, 'Супермаркеты', '2023-12-31')
        print("Траты по категории:", category_spending_json)
    else:
        logging.error("Не удалось прочитать данные из Excel-файла.")

if __name__ == "__main__":
    main()
