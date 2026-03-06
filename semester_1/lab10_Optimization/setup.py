from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "Integrate_cy.pyx",
        annotate=True
    )
)
