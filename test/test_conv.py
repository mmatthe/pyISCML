import unittest
from scipy.io import loadmat
import numpy as np
import numpy.testing as nt
import os

from pyISCML import convolutional
from .testing import assert_array_equal_ignorenan

class TestConvEncode_SameAsMatlab(unittest.TestCase):
    def _check(self, nr):
        mat = loadmat(os.path.join(os.path.dirname(__file__), 'data/ConvEncode_%d.mat' % nr))
        data = mat['bits'].flatten().astype(int)
        g = mat['g'].astype(int)
        expectedEncoded = mat['encoded'].flatten().astype(int)
        code_type = int(mat['code_type'])

        encoded = convolutional.Encode(data, g, code_type)

        nt.assert_array_almost_equal(encoded, expectedEncoded)

    def test_SameAsMatlab_1(self):
        for i in range(9):
            self._check(i+1)

class TestSisoDecode_SameAsMatlab(unittest.TestCase):
    def _check(self, nr):
        mat = loadmat(os.path.join(os.path.dirname(__file__), 'data/SisoDecode_%d.mat' % nr))
        input_c = mat['input_c'].flatten().astype(float)
        g = mat['g'].astype(np.int32)
        expectedDecoded_u = mat['decoded_u'].flatten()
        expectedDecoded_c = mat['decoded_c'].flatten()
        code_type = int(mat['code_type'])
        decoder_type = int(mat['decoder_type'])

        # print input_c[:5],
        # import pdb; pdb.set_trace()
        decoded_u, decoded_c = convolutional.SisoDecode(-input_c, g, code_type, decoder_type);

        nt.assert_array_almost_equal(-decoded_u, expectedDecoded_u, decimal=4)
        nt.assert_array_almost_equal(-decoded_c, expectedDecoded_c, decimal=4)

    def test_SameAsMatlab(self):
        for nr in range(30):
            self._check(nr+1)




if __name__ == '__main__':
    unittest.main()
