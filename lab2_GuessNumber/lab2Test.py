import unittest
import lab2Code as main


class Testlinear_search(unittest.TestCase):
    def test1(self):
        self.assertEqual(main.seq_search(5, list(range(2, 25))), (5, 4))

    def test2(self):
        self.assertEqual(main.seq_search(5, list(range(6, 25))), 'Числа нет в указанном диапазоне')

    def test3(self):
        self.assertEqual(main.seq_search([], list(range(6, 25))), 'Введите корректные данные')

    def test4(self):
        self.assertEqual(main.seq_search(5, []), 'Числа нет в указанном диапазоне')

    def test5(self):
        self.assertEqual(main.seq_search(5, ''), 'Введите корректные данные')

    def test6(self):
        self.assertEqual(main.seq_search(5, [5]), (5, 1))


class Testbinary_search(unittest.TestCase):
    def test1(self):
        self.assertEqual(main.binary_search(13, list(range(10, 50))), (13, 6))

    def test2(self):
        self.assertEqual(main.binary_search(7, list(range(-3, 3))), 'Числа нет в указанном диапазоне')

    def test3(self):
        self.assertEqual(main.binary_search('', list(range(6, 25))), 'Введите корректные данные')

    def test4(self):
        self.assertEqual(main.binary_search(13, []), 'Числа нет в указанном диапазоне')

    def test5(self):
        self.assertEqual(main.binary_search(5, None), 'Введите корректные данные')

    def test6(self):
        self.assertEqual(main.binary_search(-3, [-3]), (-3, 1))
if __name__ == '__main__':
    unittest.main()