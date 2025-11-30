import unittest
import requests
from models.user import Users
from models import Currencies,App,Author,Usercurrencies
from utils.currencies_api import get_currencies


class TestLab8(unittest.TestCase):
    #Проверка создания пользователя
    def test1(self):
        user = Users("Ivan", "101")
        self.assertEqual(user.name, "Ivan")
        self.assertEqual(user.id, "101")

    #Проверка на неккоректное имя пользователя
    def test2(self):
        with self.assertRaises(ValueError):
            Users("I", "123")

    #Проверка на создание валюты
    def test3(self):
        curr = Currencies("USD", "123", "Доллар США", 90.50, 1.0)
        self.assertEqual(curr.code, "123")
        self.assertEqual(curr.value, 90.50)

    #Проверка на неккоректный тип кода
    def test4(self):
        with self.assertRaises(ValueError):
            Currencies("123", 123, "Name", 50.0, 1.0)

    #Проверка работы модели app
    def test5(self):
        author = Author("Maksim", "P3124")
        app = App("TestApp", "1.0", author)
        self.assertEqual(app.author.name, "Maksim")

    #Проверка на неккоректный тип author
    def test6(self):
        with self.assertRaises(ValueError):
            App("TestApp", "1.0", "абвг")

    #Проверка создания Usercurrencies
    def test7(self):
        user = Users("Ivan", "123")
        curr = Currencies("456", "USD", "Доллар США", 90.50, 1.0)
        uscurr = Usercurrencies("789", "123", "456")
        self.assertEqual(uscurr.id, "789")
        self.assertEqual(uscurr.user_id, "123")
        self.assertEqual(uscurr.currency_id, "456")

    #Тест на работу функции get_currencies
    def test8(self):
        data = get_currencies(['USD'])
        self.assertIsInstance(data, dict)
        usd_info = data['USD']
        self.assertIsInstance(usd_info, tuple)
        self.assertEqual(len(usd_info), 5)
    def test9(self):
        with self.assertRaises(requests.exceptions.RequestException):
            get_currencies(['USD'], url="https//wfgewfgew9uw9f0")

