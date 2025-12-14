import timeit
import math
import concurrent.futures as ftres

from functools import partial
from Integrate import integrate as integrate_py
from Integrate_cy import integrate_cy, integrate_sin_pure_c


def integrate_async_4(f, f_integrate, executor, a: float, b: float, *, n_jobs=2, n_iter: int = 100000000):
    """
    Функция асинхронного вычисления интеграла
    :param f: Функция, чей интеграл вычисляем
    :param f_integrate: Функция вычисления интеграла
    :param executor: Управление процессами или потоками
    :param a: Левая граница
    :param b: Правая граница
    :param n_jobs: Число потоков, которые будут работать
    :n_iter: Число итераций
    :return: Значение интеграла(площадь под графиком)
    """

    if f is None:
        spawn = partial(executor.submit, f_integrate, n_iter=n_iter // n_jobs)
    else:
        spawn = partial(executor.submit, f_integrate, f, n_iter=n_iter // n_jobs)
    step = (b - a) / n_jobs
    # for i in range(n_jobs):
    # print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(list(f.result() for f in ftres.as_completed(fs)))


def benchmark_4():
    n_iter = 100_000_000
    a, b = 0, math.pi
    n_jobs = 10
    executorProcess = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    executorThread = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    print(f"Число итераций: {n_iter}")

    # 1. Чистый Python
    t_py = timeit.timeit(lambda: integrate_py(math.sin, a, b, n_iter=n_iter), number=5) / 5
    print(f"Python: {t_py:.4f} сек")

    # 2. Cython
    t_cy_f = timeit.timeit(lambda: integrate_cy(math.sin, a, b, n_iter=n_iter), number=5) / 5
    print(f"Cython (math.sin): {t_cy_f:.4f} сек (Ускорение: {t_py / t_cy_f:.2f}x)")

    # 3. Cython (Pure C)
    t_cy_pure = timeit.timeit(lambda: integrate_sin_pure_c(a, b, n_iter=n_iter), number=5) / 5
    print(f"Cython (C sin):  {t_cy_pure:.4f} сек (Ускорение: {t_py / t_cy_pure:.2f}x)")

    # 4. Cython с потоками
    t_async_threads_cy = timeit.timeit(
        lambda: integrate_async_4(None, integrate_sin_pure_c, executorThread, a, b, n_jobs=n_jobs, n_iter=n_iter),
        number=5) / 5
    print(f"Cython (C sin + Threads): {t_async_threads_cy:.4f} сек")

    # 5. Cython с процессами
    t_async_process_cy = timeit.timeit(
        lambda: integrate_async_4(None, integrate_sin_pure_c, executorProcess, a, b, n_jobs=n_jobs, n_iter=n_iter),
        number=5) / 5
    print(f"Cython (C sin + Process): {t_async_process_cy:.4f} сек")

    # 6 Python c потоками
    t_async_threads_py = timeit.timeit(
        lambda: integrate_async_4(math.sin, integrate_py, executorThread, a, b, n_jobs=n_jobs, n_iter=n_iter),
        number=5) / 5
    print(f"Python (math.sin + Threads): {t_async_threads_py:.4f} сек")

    # 7 Python с процессами
    t_async_process_py = timeit.timeit(
        lambda: integrate_async_4(math.sin, integrate_py, executorProcess, a, b, n_jobs=n_jobs, n_iter=n_iter),
        number=5) / 5
    print(f"Python (math.sin + Process): {t_async_process_py:.4f} сек")


if __name__ == "__main__":
    benchmark_4()
