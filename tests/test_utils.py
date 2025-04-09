import unittest
import pandas as pd
from datetime import datetime
import logging
import sys
from unittest.mock import patch
import os
from parameterized import parameterized  # Импортируем parameterized
from src.utils import read_excel, parse_date, setup_logging  # Импортируем функции

# Добавляем путь к директории с кодом, который нужно протестировать
sys.path.append(".")


class TestUtils(unittest.TestCase):
    EXCEL_FILE = "test_data.xlsx"  # Имя файла для тестовых данных

    @classmethod
    def setUpClass(cls):
        """Создаем тестовый Excel файл один раз для всех тестов."""
        data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
        cls.test_df = pd.DataFrame(data)
        cls.test_df.to_excel(cls.EXCEL_FILE, index=False)  # Сохраняем в файл, доступный для всех тестов класса

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовый Excel файл после всех тестов."""
        if os.path.exists(cls.EXCEL_FILE):
            os.remove(cls.EXCEL_FILE)

    def test_read_excel_success(self):
        result = read_excel(self.EXCEL_FILE)
        pd.testing.assert_frame_equal(result, self.test_df)

    def test_read_excel_file_not_found(self):
        result = read_excel("non_existent_file.xlsx")
        self.assertIsNone(result)

    @parameterized.expand([
        ("2023-10-26 10:00:00", datetime(2023, 10, 26, 10, 0, 0)),
        ("2024-01-15 14:30:00", datetime(2024, 1, 15, 14, 30, 0)),
        ("2022-12-31 23:59:59", datetime(2022, 12, 31, 23, 59, 59)),  # Добавляем еще один успешный кейс
    ])
    def test_parse_date_success(self, date_string, expected_date):
        result = parse_date(date_string)
        self.assertEqual(result, expected_date)

    @parameterized.expand([
        ("invalid date", None),
        ("12345", None),
        ("", None),  # Тест на пустую строку
        (None, None),  # Тест на None
    ])
    def test_parse_date_failure(self, date_string, expected):
        result = parse_date(date_string)
        self.assertEqual(result, expected)  # Сравниваем с None

    @patch("logging.basicConfig")
    @parameterized.expand([
        (logging.DEBUG,),
        (logging.INFO,),
        (logging.WARNING,),
    ])
    def test_setup_logging(self, level, mock_basic_config):
        setup_logging(level)
        mock_basic_config.assert_called_once_with(
            level=level, format="%(asctime)s - %(levelname)s - %(message)s"
        )


if __name__ == "__main__":
    unittest.main()
