# cython: language_level=3
from libc.math cimport sin

cpdef double integrate_cy(object f, double a, double b, long n_iter):

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    return acc

cpdef double integrate_sin_pure_c(double a, double b, long n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += sin(a + i * step) * step
    return acc

cpdef double integrate_nogil(double a, double b, int n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    with nogil:
        for i in range(n_iter):
            acc += sin(a + i * step) * step

    return acc