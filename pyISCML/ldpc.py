import numpy as np
from scipy.io import loadmat
import os

from numpy.random import RandomState

import _pyISCML

def InitializeWiMaxLDPC(rate, codedLength):
    rateDict = {}
    rateDict[5./6.] = '56'
    rateDict[3./4.] = '34'
    rateDict[1./2.] = '12'

    assert(rate in rateDict)
    rateStr = rateDict[rate]

    fn = 'ldpcMats/WiMax_%s_%d.mat' % (rateStr, codedLength);

    H = loadmat(os.path.join(os.path.dirname(__file__), fn))

    H_rows = H['H_rows']
    H_cols = H['H_cols']
    P = H['P']

    return H_rows, H_cols, P

def Encode(bits, H_rows, P):

    nldpc = bits.shape[0] + H_rows.shape[0]
    encoded = np.zeros(nldpc, dtype=np.int32)

    _pyISCML.ldpcEncode(bits, H_rows.T.copy(), P.T.copy(), encoded)

    return encoded

def MpDecode(llr, H_rows, H_cols, max_iter, dec_type, r_scale_factor=1, q_scale_factor=1, bits=None, softOut=False):
    llrOut = np.zeros((llr.shape[0], max_iter), dtype=float)
    biterrors = np.zeros((max_iter, ), dtype=np.int32)

    if bits is None:
        bits = np.zeros(llr.shape, dtype=np.int32)



    _pyISCML.MpDecode(llr, H_rows.T.copy(), H_cols.T.copy(),
                       max_iter, dec_type, r_scale_factor, q_scale_factor,
                       bits,
                       llrOut,
                       biterrors)

    if softOut:
        return llrOut.T.copy(), biterrors
    else:
        decoded = (llrOut < 0).astype(np.int32)
        return (decoded.T.copy(), biterrors)
