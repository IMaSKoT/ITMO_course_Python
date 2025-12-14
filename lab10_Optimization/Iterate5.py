import timeit
import math
import concurrent.futures as ftres
from Integrate_cy import integrate_nogil, integrate_sin_pure_c
from Iterate4 import integrate_async_4


def benchmark_5():
    n_iter = 100_000_000
    a, b = 0, math.pi
    # 1. noGIL Cython + threads
    for n_jobs in range(2, 22, 2):
        executorThread = ftres.ThreadPoolExecutor(max_workers=n_jobs)
        time_cy = timeit.timeit(
            lambda: integrate_async_4(None, integrate_nogil, executorThread, a, b, n_jobs=n_jobs, n_iter=n_iter),
            number=5) / 5
        print(f"noGIL, : {n_jobs} потоков: {time_cy:.4f} сек")

    # 2. GIL Cython + process
    for n_jobs in range(2, 22, 2):
        executorProcess = ftres.ProcessPoolExecutor(max_workers=n_jobs)
        time_cy = timeit.timeit(
            lambda: integrate_async_4(None, integrate_sin_pure_c, executorProcess, a, b, n_jobs=n_jobs, n_iter=n_iter),
            number=5) / 5
        print(f"GIL, : {n_jobs} процессов: {time_cy:.4f} сек")


if __name__ == "__main__":
    benchmark_5()
