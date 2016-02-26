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


class LdpcCodeTests(unittest.TestCase):
    def _testDecReverseEnc(self, Code, numBitFlips=0):
        source = Code.createDataSource()
        dec = Code.createDecoder()

        payload, enc = source.generate(1, 2304-Code._puncturing)

        if numBitFlips > 0:
            enc[:numBitFlips] *= -1

        payloadEst = dec.decode(4*enc.astype(float).flatten())

        assert_array_equal_ignorenan(payloadEst, payload)
        # nt.assert_array_equal(payloadEst, payload)


    def test_decodeReversesEncode(self):
        Code = ldpc.LdpcCode(rate=5./6.)
        self._testDecReverseEnc(Code)


    def test_interleaver(self):
        Code = ldpc.LdpcCode(rate=5./6., interleaverIndex=0)
        self._testDecReverseEnc(Code)

    def test_effectiveRate(self):
        Code = ldpc.LdpcCode(rate=5./6.)
        self.assertEqual(Code.effectiveRate(2304), 5./6.)

        puncturing = 56  # Puncture 56 bits away
        Code = ldpc.LdpcCode(rate=5./6., puncturing=puncturing)
        expRate = 2304 * 5. / 6 / (2304 - puncturing)
        self.assertEqual(Code.effectiveRate(2304-puncturing), expRate)

    def test_puncturingTX(self):
        puncturing = 56
        Code = ldpc.LdpcCode(rate=5./6., puncturing=puncturing)

        payload, bpsk = Code.createDataSource().generate(1, 2304-56)
        self.assertEqual(bpsk.shape[0], 2304-56)

    def test_puncturingWithErrorsIsDecodable(self):
        puncturing = 56
        Code = ldpc.LdpcCode(rate=5./6., puncturing=puncturing, interleaverIndex=1)
        self._testDecReverseEnc(Code, 10)

    def test_punctureDepuncture(self):
        puncturing = 56
        Code = ldpc.LdpcCode(rate=5./6., puncturing=puncturing)
        source = Code.createDataSource()
        dec = Code.createDecoder()

        llr = np.arange(2304)+20
        punctured = source._puncture(llr, 2304*5/6)
        unpunctured = dec._depuncture(punctured)
        step = int((2304 * 1 / 6)/56)
        pIndx = np.arange(56).astype(int) * step

        expected = llr.copy(); expected[pIndx + 2304*5/6] = 0

        nt.assert_array_equal(expected, unpunctured)

    def test_decoderReturnUncoded(self):
        Code = ldpc.LdpcCode(rate=5./6., returnUncoded=True)
        source = Code.createDataSource()
        dec = Code.createDecoder()

        payload, qam = source.generate(1, 2304-Code._puncturing)

        payloadEst = dec.decode(4*qam.astype(float).flatten())

        assert_array_equal_ignorenan(payloadEst, payload)



if __name__ == '__main__':
    # print "Attach debugger and press Enter"
    # X = raw_input()
    unittest.main()
