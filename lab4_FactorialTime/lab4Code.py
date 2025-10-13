import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
@lru_cache()
def fact_recursive(n: int) -> int:
    """
    Рекурсивный факториал
    :param n: Число, факториал которого нужно посчитать
    :return: Факториал числа
    """
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)

@lru_cache()
def fact_iterative(n: int) -> int:
    """
    Нерекурсивный факториал
    :param n: Число, факториал которого нужно посчитать
    :return: Факториал числа
    """
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def benchmark(func, n, number=1, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
    return min(times)

def main():
    test_data = list(range(10, 300, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
      res_recursive.append(benchmark(fact_recursive, n, repeat=5, number=1000))
      res_iterative.append(benchmark(fact_iterative, n, repeat=5, number=1000))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()