import numpy as np
from scipy.io import loadmat
import os

from numpy.random import RandomState

import _pyISCML

def InitializeWiMaxLDPC(rate, codedLength):
    """Initialies the WiMax LDPC encoder/decoder

The calling syntax is:
    (H_rows, H_cols, P) = InitializeWiMaxLDPC(rate, length)

where:
    H_rows : a M-row matrix containing the indices of the non-zero
             rows of H, excluding the dual-diagonal portion of H.
    H_cols : a (N-M)+z-row matrix, contaiing the indices of the
             non-zero rows of H.
    P      : a z times z matrix used in encoding.

    rate   : the code rate. Can be either 1/2, 3/4 or 5/6
    length : the block length of the code. Must be element of
             arange(576, 2304+96, 96)

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

"""
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
    """LdpcEncode incodes an LDPC codeword. Code must be an
"eIRA-LDPC" type code, such as the one in the DVB-S2 standard, or
WiMax standard.

The calling syntax is:
    codeword = LdpcEncode(bits, H_rows, P)

where:
    codeword = the encoded codeword

    data   : a vector containing the data
    H_rows : a M-row matrix containing the indices of the non-zero
             rows of H, excluding the dual-diagonal part.
    P      : z times z matrix usde to generate the first z check bits
             for WiMax

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

"""

    nldpc = bits.shape[0] + H_rows.shape[0]
    encoded = np.zeros(nldpc, dtype=np.int32)

    _pyISCML.ldpcEncode(bits, H_rows.T.copy(), P.T.copy(), encoded)

    return encoded

def MpDecode(llr, H_rows, H_cols, max_iter, dec_type,
             r_scale_factor=1, q_scale_factor=1, bits=None,
             softOut=False):
    """MpDecode decodes a block code (e.g. LDPC) usin gthe message passing algorithm.

The calling syntax is:
    [output, errors] = MpDecode(input, H_rows, H_cols, max_iter,
                                dec_type, r_scale_factor,
                                q_scale_factor, bits, softOut)

Where:
    output     : matrix of dimension maxiter x N that has the decoded
                 code bits for each iteration.
    errors     : vector shownig the number of bit errors in each
                 iteration (if bits are passed to the function)

    input      : LLR denoting the decoder input
    H_cols     : a N row matrix specifying the locations of the
                 non-zero entries of the H matrix. The number of
                 columns in the matrix is the column weight
                 OR
                 a K row matrix specifying locations of the nonzero
                 entries in each coulmn of an extended IRA type
    H_rows     : a N-K row matrix specifying the locations of the
                 nonzero entries in each row of the H matrix. The
                 number or columns in the matrix is the max row
                 weight, unless this is for an H1 matrix, in which
                 case the last n-k columns of the H matrix are equal
                 to a known H2 matrix.
    max_iter   : number of Ldpc iterations.
    r_scale_factor :  amount to scale extrinsic output of c-nodes in
                      min-sum decoding
    q_scale_factor :  amount to scale extrinsic output of v-nodes in
                      min-sum decoding (default = 1)
    bits       : a vector containing the data bits (used for counting
                 errors and for early halting). Default: all-zeros
    softOut    : if true, decoder returns soft-output, i.e. LLR values
                 instead of hard bits.


This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
"""

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
