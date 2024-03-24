from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("chess", ["chess.pyx"])
]

setup(
    ext_modules = cythonize(extensions)
)
