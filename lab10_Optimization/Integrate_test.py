import pytest
import math
from Integrate import integrate


# Проверка примера из задания
def test_1():
    result = integrate(math.cos, 0, math.pi / 2, n_iter=100)
    assert round(result, 5) == 1.00783


# Проверка интеграла синуса
def test_2():
    result = integrate(math.sin, 0, math.pi, n_iter=1000)
    assert result == pytest.approx(2.0, abs=1e-2)


# Проверка на нулевой интервал
def test_3():
    assert integrate(math.cos, 10, 10) == 0.0


# Проверка линейной функции f(x) = x
def test_4():
    result = integrate(lambda x: x, 0, 10, n_iter=1000)
    assert result == pytest.approx(50.0, rel=1e-2)
