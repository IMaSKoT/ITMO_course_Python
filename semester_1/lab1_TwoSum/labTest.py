import unittest
import labCode as main
class Testf(unittest.TestCase):
    #Обычный тест 1
    def test1(self):
        self.assertEqual(main.f([2, 7, 11, 15], 9),[0,1])
    #Обычный тест 2
    def test2(self):
        self.assertEqual(main.f([3, 2, 4], 6), [1, 2])
    #Обычный тест 3
    def test3(self):
        self.assertEqual(main.f([3, 3], 6), [0, 1])
    #Тест с отсутствием ответа
    def test4(self):
        self.assertEqual(main.f([2, 3, 4], 1), None)
    #Тест на неккоректный тип данных внутри массива
    def test5(self):
        self.assertEqual(main.f([2, 3, 4, 13, -1.1], 5), None)
    #Тест на неккоректный тип данных внутри массива 2 (строка)
    def test6(self):
        self.assertEqual(main.f([2, 3, '4', 13, 0], 5), None)
    #Тест на неккоректный тип данных внутри массива 3 (список)
    def test7(self):
        self.assertEqual(main.f([2, 3, 4, [], 2], 5), None)
    #Тест на неккоректный тип данных внутри массива 4 (булевый тип)
    def test8(self):
        self.assertEqual(main.f([2, 3, 4, 13, True], -3), None)
    #Тест на пустой список
    def test9(self):
        self.assertEqual(main.f([], 9), None)
    #Тест на неккоректный тип nums
    def test10(self):
        self.assertEqual(main.f(75, 75), None)
    #Тест на неккоректный тип target
    def test11(self):
        self.assertEqual(main.f([0,1,2,3], 7.5), None)




if __name__ == '__main__':
    unittest.main()