import unittest
from scipy.io import loadmat
import os
import numpy.testing as nt
import numpy as np
from .testing import assert_array_equal_ignorenan

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


if __name__ == '__main__':
    # print "Attach debugger and press Enter"
    # X = raw_input()
    unittest.main()
