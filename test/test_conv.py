import unittest
from scipy.io import loadmat
import numpy as np
import numpy.testing as nt
import os

from coding import convolutional
from utils.testing import assert_array_equal_ignorenan

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

class TestConvDataGenerator(unittest.TestCase):
    def _getSource(self, g, returnUncoded=False):
        Code = convolutional.ConvolutionalCode(g, returnUncoded=returnUncoded)
        source = Code.createDataSource()
        return source

    def test_raisesOnWrongLength(self):
        source = self._getSource(g=np.ones((3, 4)))
        self.assertRaises(RuntimeError, source.generate,  1, 100)

    def test_correctPayloadLength_BPSK_noUncoded(self):
        source = self._getSource(g=np.ones((3, 4)), returnUncoded=False)

        payload, enc = source.generate(1, 90)

        self.assertEqual(payload.shape, (90/3-3, 1))
        self.assertEqual(enc.shape, (90, 1))

    def test_correctPayloadLength_BPSK_withUncoded(self):
        source = self._getSource(g=np.ones((3, 4)), returnUncoded=True)

        payload, enc = source.generate(1, 90)

        self.assertEqual(payload.shape, (90, 2))
        f = np.zeros((90/3-3, 1), dtype=bool)
        t = np.ones((2*90 / 3+3, 1), dtype=bool)
        nt.assert_array_equal(np.vstack([f, t]), np.isnan(payload[:,0,None]))
        self.assertEqual(enc.shape, (90, 1))

    def test_correctPayloadLength_64QAM_withUncoded(self):
        source = self._getSource(g=np.ones((3, 4)), returnUncoded=True)

        payload, enc = source.generate(6, 100)

        self.assertEqual(payload.shape, (100*6,2))
        f = np.zeros((100*6/3-3, 1), dtype=bool)
        t = np.ones((2*(100*6) / 3+3, 1), dtype=bool)
        nt.assert_array_equal(np.vstack([f, t]), np.isnan(payload[:,0,None]))
        self.assertEqual(enc.shape, (100,1))

    def test_correctPayloadLength_64QAM_noUncoded(self):
        source = self._getSource(g=np.ones((3, 4)), returnUncoded=False)

        payload, enc = source.generate(6, 100)

        self.assertEqual(payload.shape, (100*6/3-3,1))
        self.assertEqual(enc.shape, (100,1))


class TestConvCode(unittest.TestCase):
    def _decReverses(self, returnUncoded=False, interleaverIndex=None):
        g = np.array([[1, 0, 1, 1, 0, 1, 1],[1, 1, 1, 1, 0, 0, 1]]);
        Code = convolutional.ConvolutionalCode(g=g, code_type=0, returnUncoded=returnUncoded, interleaverIndex=interleaverIndex)
        source = Code.createDataSource()
        dec = Code.createDecoder()

        payload, enc = source.generate(1, 600)
        payloadEst = dec.decode(enc.astype(float).flatten())

        assert_array_equal_ignorenan(payloadEst[:,0], payload[:,0])

    def test_decodeReversesEncoden_noUncoded(self):
        self._decReverses(returnUncoded=False)

    def test_decodeReversesEncoden_withUncoded(self):
        self._decReverses(returnUncoded=True)

    def test_decodeReversesEncode_withInterleaving(self):
        self._decReverses(interleaverIndex=1)

    def test_decodeReturnInterleavedUncoded(self):
        g = np.array([[1, 0, 1, 1, 0, 1, 1],[1, 1, 1, 1, 0, 0, 1]]);
        Code = convolutional.ConvolutionalCode(g=g, code_type=0, returnUncoded=True, interleaverIndex=1)
        source = Code.createDataSource()
        dec = Code.createDecoder()

        payload, enc = source.generate(1, 600)
        payloadEst = dec.decode(enc.astype(float).flatten(), softOut=True)

        assert_array_equal_ignorenan(enc.flatten() < 0, payloadEst[:,-1] < 0)
        assert_array_equal_ignorenan(payload==1, payloadEst < 0)




if __name__ == '__main__':
    unittest.main()
