import math
import timeit
import pytest


def integrate(f, a: float, b: float, *, n_iter: int = 10000000) -> float:
    """
    Функция, вычисляющая интеграл методом прямоугольников
    :param f: Функция, чей интеграл вычисляем
    :param a: Левая граница
    :param b: Правая граница
    :n_iter: Число итераций
    :return: Значение интеграла(площадь под графиком)
    >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5)
    1.00783
    """
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


if __name__ == '__main__':
    # Тест 1 и 2(Просто вывод времени и результата)
    print('Результат 1:', (integrate(math.cos, 0, math.pi, n_iter=100)))
    print('Время 1:', (timeit.timeit(lambda: integrate(math.cos, 0, math.pi), number=5) / 5))
    print('Результат 2:', integrate(math.sin, 0, 100))
    print('Время 2:', (timeit.timeit(lambda: integrate(math.sin, 0, 100), number=5) / 5))
    pytest.main()
