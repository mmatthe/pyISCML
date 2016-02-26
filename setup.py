from distutils.core import setup, Extension
import numpy
import os

if os.name == 'nt':
    extra_compile_args = []
else:
    extra_compile_args = ['--std=c++11']
codingExt = Extension("_pyISCML",
                      sources=["cpp/pyISCML.i", "cpp/LdpcEncode.cpp", "cpp/MpDecode.cpp", "cpp/ConvEncode.cpp", "cpp/SisoDecode.cpp"],
                      include_dirs=[numpy.get_include()],
                      define_macros=[('SWIG_PYTHON_INTERPRETER_NO_DEBUG', 1)],
                      language="c++",
                      extra_compile_args=extra_compile_args)

exts = [codingExt]

setup(ext_modules=exts)
