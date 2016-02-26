import codingExt
import numpy as np
from numpy.random import RandomState

from wlib.transmitter import DataGenerator
from wlib import qammodulation as mod

class Code(object):
    def createDataSource(self):
        raise NotImplementedError()

    def createDecoder(self):
        raise NotImplementedError()

class ConvolutionalCode(Code):
    def __init__(self, g, code_type=0, returnUncoded=False, interleaverIndex=None):
        self._g = g
        self._code_type = code_type
        self._returnUncoded = returnUncoded
        self._uncodedCopies = 1
        self._interleaverIndex = interleaverIndex
        self._intlList = {}

    def createDataSource(self):
        return ConvolutionalDataGenerator(self)

    def createDecoder(self):
        return ConvolutionalDecoder(self)

    def _getInterleaver(self, length):
        if length in self._intlList:
            return self._intlList[length]

        if self._interleaverIndex is None:
            intl = np.arange(length)
            intlI = intl.copy()
        else:
            R = RandomState(self._interleaverIndex)
            intl = np.arange(length)
            R.shuffle(intl)
            intlI = intl.argsort()
        self._intlList[length] = (intl, intlI)
        return intl, intlI



class ConvolutionalDataGenerator(DataGenerator):
    def __init__(self, CodeObj):
        self._Code = CodeObj
        assert(type(CodeObj) is ConvolutionalCode)

    def generate(self, mu, numSymbols):
        g = self._Code._g

        numCodedBits = mu * numSymbols
        if numCodedBits % g.shape[0] != 0:
            raise RuntimeError("Impossible bit length, needs to be dividable by rate")
        numPayloadBits = (numCodedBits / g.shape[0]) - g.shape[1] + 1

        payload = (np.random.randn(numPayloadBits) > 0).astype(int)
        encoded = Encode(payload, g, self._Code._code_type)
        intl, intlI = self._Code._getInterleaver(encoded.shape[0])
        encoded = encoded[intl]

        bits = encoded.reshape((-1, mu))
        if mu == 1:
            qam = 1-2*bits
        else:
            qam = mod.bits2qam(bits, 2**mu)

        if not self._Code._returnUncoded:
            resultPayload = payload.reshape((-1,1))
        else:
            resultPayload = float("nan") * np.zeros((encoded.shape[0], 1+self._Code._uncodedCopies))
            resultPayload[:payload.shape[0],0] = payload
            for i in range(self._Code._uncodedCopies):
                resultPayload[:,1+i] = encoded
        return resultPayload, qam.reshape((-1,1))


class ConvolutionalDecoder(object):
    def __init__(self, CodeObj):
        self._Code = CodeObj
        assert(type(CodeObj) is ConvolutionalCode)

    def decode(self, llr, softOut=False, returnUncoded=None):
        intl, intlI = self._Code._getInterleaver(llr.shape[0])
        dec_u, dec_c = SisoDecode(llr[intlI], self._Code._g.astype(np.int32), self._Code._code_type, 4)

        retUnc = self._Code._returnUncoded
        if returnUncoded is not None:
            retUnc = returnUncoded

        if not retUnc:
            result = dec_u.reshape((-1,1))
        else:
            result = float("nan") * np.zeros((dec_c.shape[0], 2))
            result[:dec_u.shape[0],0] = dec_u
            result[:,1] = dec_c[intl]

        if softOut:
            return result
        else:
            return (result < 0).astype(int)



def Encode(bits, g, codeType):
    if codeType < 2:
        outLen = g.shape[0]*(bits.shape[0] + g.shape[1]-1)
    else:
        outLen = g.shape[0]*bits.shape[0]
    encoded = codingExt.ConvEncode(bits.astype(np.int32), g.astype(np.int32), codeType, outLen);
    return encoded

def SisoDecode(input_c, g, code_type, decoder_type):
    input_u = np.zeros(input_c.shape[0]/g.shape[0]-g.shape[1]+1, dtype=float)
    assert code_type != 2, "Tail-biting not supported for SISO decode"

    decoded_u = np.zeros(input_u.shape)
    decoded_c = np.zeros(input_c.shape)
    codingExt.SisoDecode(-input_u, -input_c, g, code_type, decoder_type, decoded_u, decoded_c)
    return -decoded_u, -decoded_c

    pass
