import pandas as pd
import logging
from datetime import datetime


def setup_logging(level=logging.INFO):
    """Настраивает логирование."""
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')


def read_excel(file_path: str) -> pd.DataFrame:
    """
    Читает Excel-файл и возвращает DataFrame.
    Args:
        file_path: Путь к Excel-файлу.
    Returns:
        DataFrame с данными из Excel-файла.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Ошибка при чтении Excel-файла: {e}")
        return None


def parse_date(date_string: str) -> datetime:
    """Парсит строку с датой в объект datetime."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')  # Пример формата
    except ValueError as e:
        logging.warning(f"Не удалось распарсить дату: {date_string}.  Ошибка: {e}")
        return None
