import unittest
import pandas as pd
from datetime import datetime
import logging
from unittest.mock import patch
import sys
from src.utils import read_excel, parse_date, setup_logging  # Импортируем функции

# Добавляем путь к директории с кодом, который нужно протестировать
sys.path.append(".")


class TestUtils(unittest.TestCase):

    def test_read_excel_success(self):
        # Создаем DataFrame для теста
        data = {"col1": [1, 2], "col2": [3, 4]}
        df = pd.DataFrame(data)
        df.to_excel("tests.xlsx", index=False)
        result = read_excel("tests.xlsx")
        pd.testing.assert_frame_equal(result, df)

    def test_read_excel_file_not_found(self):
        result = read_excel("non_existent_file.xlsx")
        self.assertIsNone(result)

    def test_parse_date_success(self):
        date_string = "2023-10-26 10:00:00"
        expected_date = datetime(2023, 10, 26, 10, 0, 0)
        result = parse_date(date_string)
        self.assertEqual(result, expected_date)

    def test_parse_date_failure(self):
        date_string = "invalid date"
        result = parse_date(date_string)
        self.assertIsNone(result)

    @patch("logging.basicConfig")
    def test_setup_logging(self, mock_basic_config):
        setup_logging(logging.DEBUG)
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )


if __name__ == "__main__":
    unittest.main()
