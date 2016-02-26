SET VS90COMNTOOLS=%VS120COMNTOOLS%
rem python setup.py build_ext --inplace --swig-cpp --debug
rem copy _codingExt_d.pyd _codingExt.pyd

python setup.py build_ext --inplace --swig-cpp

rem pause