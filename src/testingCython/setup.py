from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("chess_board", ["chess_board.pyx"], include_dirs=[np.get_include()])
]

setup(
    ext_modules = cythonize(extensions)
)