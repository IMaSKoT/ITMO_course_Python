import unittest
import sys
import os
from unittest.mock import MagicMock

from lab9_CRUD.controllers import CurrencyRatesCRUD, CurrencyController


class TestCurrencyControllerMock(unittest.TestCase):
    """
    Класс тестирования CurrencyController
    Проверяет логику работы с валютами, имитируя поведение базы данных
    """

    def setUp(self):
        """
        Подготовка окружения перед каждым тестом.
        Создает Mock-объект базы данных и инициализирует контроллер.
        """
        self.mock_db = MagicMock(spec=CurrencyRatesCRUD)
        self.controller = CurrencyController(self.mock_db)

    def test_list_currencies(self):
        """
        Тестирование метода Read (получение списка валют)
        Проверяет, что контроллер корректно возвращает данные, полученные от БД.
        """
        expected = [{'id': 1, 'char_code': 'USD', 'value': 90.0}]
        self.mock_db._read_currencies.return_value = expected
        result = self.controller.list_currencies()
        self.assertEqual(result, expected, "Контроллер должен возвращать данные из БД без искажений")
        self.mock_db._read_currencies.assert_called_once()

    def test_update_currency_success(self):
        """
        Тестирование метода Update (обновление курса).
        Проверяет, что контроллер вызывает метод обновления БД с правильными параметрами.
        """
        self.mock_db._update_currency_value.return_value = True
        result = self.controller.update_currency('USD', 100.0)
        self.assertTrue(result, "Метод должен вернуть True при успешном обновлении")
        self.mock_db._update_currency_value.assert_called_with('USD', 100.0)

    def test_delete_currency(self):
        """
        Тестирование метода Delete (удаление валюты)
        Проверяет, что контроллер корректно передает код валюты на удаление в БД
        """
        self.mock_db._delete_currency.return_value = True
        result = self.controller.delete_currency('USD')
        self.assertTrue(result, "Метод должен вернуть True при успешном удалении")
        self.mock_db._delete_currency.assert_called_with('USD')


if __name__ == '__main__':
    unittest.main()
