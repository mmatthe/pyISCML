import unittest
from scipy.io import loadmat
import numpy as np
import numpy.testing as nt
import os

from pyISCML import convolutional
from .utils import assert_array_equal_ignorenan

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


class TestEncodeDecode(unittest.TestCase):
    def _testEncDec(self, payload, g, code_type, decoder_type):
        payload = payload.astype(int)
        encoded = convolutional.Encode(payload, g, code_type)
        llr = 1 - 2*encoded
        decoded_u, decoded_c = convolutional.SisoDecode(llr, g, code_type, decoder_type)

        decodedBits = (decoded_u < 0).astype(int)
        decodedCode = (decoded_c < 0).astype(int)
        nt.assert_array_equal(payload, decodedBits)
        nt.assert_array_equal(encoded, decodedCode)


    def test_halfRate(self):
        g = np.array([[1, 0, 0, 1, 1],
                      [1, 1, 0, 1, 0]])
        for code_type in [0, 1]:
            for decoder_type in range(5):
                self._testEncDec(np.random.randn(1000) < 0, g, code_type=0, decoder_type=1)

    def test_thirdRateRate(self):
        g = np.array([[1, 0, 0, 1, 1],
                      [1, 1, 0, 1, 0],
                      [1, 0, 1, 0, 1]])
        for code_type in [0, 1]:
            for decoder_type in range(5):
                self._testEncDec(np.random.randn(1000) < 0, g, code_type=0, decoder_type=1)




if __name__ == '__main__':
    unittest.main()
