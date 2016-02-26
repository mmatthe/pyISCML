# pyISCML
Python Bindings for Coded Modulation Library https://github.com/wvu-wcrl/CML

This project aims to provide bindings to the encoders and decoders of
the CML for Python. Currently supported functions:

Keywords: Python, channel coding, coding, LDPC, convolutional code,
signal processing, coded modulation library.

## LDPC WiMax Codes
- `ldpc.InitializeWiMaxLDPC` - create generator and decoder matrices for WiMax-Compatible LDPC codes
- `ldpc.Encode` - Encode payload bits with LDPC code
- `lpdc.MpDecode` - Soft-in-soft-out decoding of LDPC codes

## Convolutional Codes
- `convolutional.Encode` - encode bit sequence with given generator polynomial
- `convolutional.SisoDecode` - soft-in-soft-out (BCJR) decode of convolutional code

Feel free to add more bindings. Check the files under `test/`, how the functions are to be called.

## Installation:
- Prerequisites:
    - Swig
    - Numpy, Scipy
	- a working C++11 compliant compiler
- just type `python setup.py build`. This will build the extension
  using swig.
- then run `python -m unittest discover` to run the automated tests to
  see if it compiled correctly.

Currently tested under Windows with Python-2.7.9, using Visual Studio
2013 compiler backend.
