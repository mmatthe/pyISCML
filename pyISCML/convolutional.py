import _pyISCML
import numpy as np
from numpy.random import RandomState


def Encode(bits, g, codeType):
    if codeType < 2:
        outLen = g.shape[0]*(bits.shape[0] + g.shape[1]-1)
    else:
        outLen = g.shape[0]*bits.shape[0]
    encoded = _pyISCML.ConvEncode(bits.astype(np.int32), g.astype(np.int32), codeType, outLen);
    return encoded

def SisoDecode(input_c, g, code_type, decoder_type):
    input_u = np.zeros(input_c.shape[0]/g.shape[0]-g.shape[1]+1, dtype=float)
    assert code_type != 2, "Tail-biting not supported for SISO decode"

    decoded_u = np.zeros(input_u.shape)
    decoded_c = np.zeros(input_c.shape)
    _pyISCML.SisoDecode(-input_u, -input_c, g, code_type, decoder_type, decoded_u, decoded_c)
    return -decoded_u, -decoded_c

    pass
