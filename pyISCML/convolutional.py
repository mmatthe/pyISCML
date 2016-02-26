import _pyISCML
import numpy as np
from numpy.random import RandomState


def Encode(bits, g, codeType):
    """Encodes a NSC or RSC convolutional code with a tail.

The calling syntax is:
    output = Encode(input, g_encoder, code_type)

Where:
    output     : code word

    input      : data word
    g_encoder  : generator matrix for convolutional code
                 (If RSC, then feedback polynomial is first)

    code_type  : = 0 for recursive systematic convolutional (RSC) code (default)
                 = 1 for non-systematic convolutional (NSC) code
                 = 2 for tail-biting NSC code

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
"""
    if codeType < 2:
        outLen = g.shape[0]*(bits.shape[0] + g.shape[1]-1)
    else:
        outLen = g.shape[0]*bits.shape[0]
    encoded = _pyISCML.ConvEncode(bits.astype(np.int32), g.astype(np.int32), codeType, outLen);
    return encoded

def SisoDecode(input_c, g, code_type, decoder_type):
    """% SisoDecode performs soft-in/soft-out decodeing of a convolutional code.

The calling syntax is:
     (output_u, output_c) = SisoDecode(input_c, g_encoder, code_type, dec_type)

Where:
    output_u    : LLR of the data bits
    output_c    : LLR of the code bits

    input_c     : APP of the code bits
    g_encoder   : generator matrix for convolutional code
                 (If RSC, then feedback polynomial is first)

    code_type   : 0 for RSC outer code (default)
                : 1 for NSC outer code
    dec_type    : the decoder type:
                  = 0 For linear approximation to log-MAP (DEFAULT)
                  = 1 For max-log-MAP algorithm (i.e. max*(x,y) = max(x,y) )
                  = 2 For Constant-log-MAP algorithm
                  = 3 For log-MAP, correction factor from small
                      nonuniform table and interpolation
                  = 4 For log-MAP, correction factor uses C function
                      calls (slow)

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
"""

    input_u = np.zeros(input_c.shape[0]/g.shape[0]-g.shape[1]+1, dtype=float)
    assert code_type != 2, "Tail-biting not supported for SISO decode"

    decoded_u = np.zeros(input_u.shape)
    decoded_c = np.zeros(input_c.shape)
    _pyISCML.SisoDecode(-input_u, -input_c, g, code_type, decoder_type, decoded_u, decoded_c)
    return -decoded_u, -decoded_c

    pass
