from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("piece_rules", ["piece_rules.pyx"]),
    Extension("piece", ["piece.pyx"]),
    Extension("chess_board", ["chess_board.pyx"])
]

setup(
    ext_modules = cythonize(extensions)
)
