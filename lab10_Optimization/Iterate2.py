import concurrent.futures as ftres
import math
import timeit
from Integrate import integrate
from functools import partial


def integrate_async(f, a: float, b: float, *, n_jobs=2, n_iter: int = 10000000):
    """
    Функция вычисления интеграла асинхронно с использованием потоков
    :param f: Функция, чей интеграл вычисляем
    :param a: Левая граница
    :param b: Правая граница
    :param n_jobs: Число потоков, которые будут работать
    :n_iter: Число итераций
    :return: Значение интеграла(площадь под графиком)
    """

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    step = (b - a) / n_jobs
    # for i in range(n_jobs):
    # print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(list(f.result() for f in ftres.as_completed(fs)))


if __name__ == '__main__':
    print('Результат:', integrate_async(math.sin, 0, math.pi))
    for n in range(2, 20, 2):
        print(f'Время для {n} потоков:',
              timeit.timeit(lambda: integrate_async(math.sin, 0, math.pi, n_jobs=n), number=5) / 5)
