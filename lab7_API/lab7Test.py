import io
import unittest
import lab7Code as main


class TestGetCurrencies(unittest.TestCase):

    # Тест: Одна корректная валюта
    def test1(self):
        result = main.get_currencies(['USD'])
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['USD'], (int, float))

    # Тест: Несколько валют
    def test2(self):
        result = main.get_currencies(['USD', 'EUR'])
        self.assertEqual(len(result), 2)

    # Тест: Неправильная валюта
    def test3(self):
        with self.assertRaises(KeyError):
            main.get_currencies(['абвг'])

    # Тест: Неправильный адрес
    def test4(self):
        with self.assertRaises(ConnectionError):
            main.get_currencies(['USD'], url='http/////')


class TestDecorator(unittest.TestCase):
    # Тест: Успешная работа функции
    def test1(self):
        self.stream = io.StringIO()

        @main.logger(handle=self.stream)
        def test_function(x):
            return x ** 2

        test_function(2)
        content = self.stream.getvalue()
        self.assertIn("INFO: Запуск функции test_function с аргументами (2,) {}\n"
                      f"INFO: Функция test_function успешно завершена. Результат: 4", content)

    # Тест: Ошибка в работе функции
    def test2(self):
        self.stream = io.StringIO()

        @main.logger(handle=self.stream)
        def test_function(x):
            return x ** 2

        with self.assertRaises(TypeError):
            test_function('абв')
        content = self.stream.getvalue()
        self.assertRegex(content, "ERROR")
