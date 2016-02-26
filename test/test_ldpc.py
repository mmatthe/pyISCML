import unittest
from scipy.io import loadmat
import os
import numpy.testing as nt
import numpy as np
from .utils import assert_array_equal_ignorenan

import pyISCML.ldpc as ldpc


class EncodeTestLikeMatlab(unittest.TestCase):
    def test_rate56(self):
        mat = loadmat(os.path.join(os.path.dirname(__file__), 'data/ldpc56_2304.mat'))
        bits = mat['bits'].flatten()
        encoded = mat['encoded'].flatten()

        (H_rows, H_cols, P) = ldpc.InitializeWiMaxLDPC(5./6., 2304)

        encoded2 = ldpc.Encode(bits, H_rows, P)
        nt.assert_array_almost_equal(encoded, encoded2)

class MpDecodeLikeMatlab(unittest.TestCase):
    def _testFile(self, fn):
        mat = loadmat(os.path.join(os.path.dirname(__file__), 'data/%s' % fn))
        llr = mat['llr'].flatten()
        bits = mat['bits'].flatten()
        H_rows = mat['H_rows']
        H_cols = mat['H_cols']

        dec = mat['dec']
        errors = mat['errors'].flatten()

        (dec2, errors2) = ldpc.MpDecode(llr, H_rows, H_cols, 100, 0, 1, 1, bits);
        nt.assert_array_equal(errors2, errors)
        nt.assert_array_equal(dec2, dec)

    def test_allFiles(self):
        d = os.path.join(os.path.dirname(__file__), 'data')
        files = os.listdir(d)
        for f in files:
            if f.startswith('MpDecode'):
                self._testFile(f)

class TestEncodeDecode(unittest.TestCase):
    def _testEncDec(self, rate, ln, dec_type):
        (H_rows, H_cols, P) = ldpc.InitializeWiMaxLDPC(rate, ln)
        payload = (np.random.randn(rate * ln) < 0).astype(int)

        encoded = ldpc.Encode(payload, H_rows, P)
        llr = 1-2*encoded
        llr[2] *= -1
        llr[50] *= -1

        (decoded, errors) = ldpc.MpDecode(4*llr, H_rows, H_cols,
                                          max_iter=100, dec_type=0, r_scale_factor=1, q_scale_factor=1)
        nt.assert_array_equal(decoded[-1,:], encoded)
        nt.assert_array_equal(decoded[-1, :rate*ln], payload)

    def test_1(self):
        rate = 5./6.
        ln = 2304

        for rate in [1./2., 3./4., 5./6.]:
            for dec_type in [0, 1]:
                self._testEncDec(rate, ln, dec_type)



if __name__ == '__main__':
    # print "Attach debugger and press Enter"
    # X = raw_input()
    unittest.main()
