import unittest
import lab5Code as main

class Testgen_bin_tree(unittest.TestCase):
    # Обычный тест с height = 0
    def test1(self):
        self.assertEqual(main.gen_bin_tree(0, 17),
                         {'17': []})
    # Обычный тест с height = 1

    def test2(self):
        self.assertEqual(main.gen_bin_tree(1, 17),
                         {'17': [{'169': []}, {'40': []}]})

    # Обычный тест с root = 1, height = 1

    def test3(self):
        self.assertEqual(main.gen_bin_tree(1, 1),
                         {'1': [{'9': []}, {'8': []}]})

    # Тест на неправильно введенный height

    def test4(self):
        self.assertEqual(main.gen_bin_tree('', 17), None)

    # Тест на неправильно введенный root

    def test5(self):
        self.assertEqual(main.gen_bin_tree(3, []), None)

    # Тест на неправильно введенный l_b

    def test6(self):
        self.assertEqual(main.gen_bin_tree(3, 17, l_b=None), None)

    # Тест на неправильно введенный r_b

    def test7(self):
        self.assertEqual(main.gen_bin_tree(3, 17, r_b=print()), None)

    # Тест на отрицательый height

    def test8(self):
        self.assertEqual(main.gen_bin_tree(-1, 17),
                         {'17': []})