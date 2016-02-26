#include <stdlib.h>

#include <vector>
#include <iostream>

#include "cmlIncludes/convolutional.h"

extern "C" void ConvEncode(int* bits, int sizeBits,
			   int* g, int sizeG1, int sizeG2,
			   int codeType,
			   int* encoded_out, int sizeOut)
{
   int nn = sizeG1;
   int KK = sizeG2;
   int mm = KK -1;
   int max_states = 1 << mm;

   int DataLength = sizeBits;
   int CodeLength = sizeOut;
   std::vector<int> g_encoder(nn, 0);

   for (int i = 0; i < nn; i++)
   {
      for (int j = 0; j < KK; j++)
      {
	 int elm = g[j + KK*i];
	 if (elm != 0)
	    g_encoder[i] += (1 << (KK-j-1));
      }
   }

   std::vector<int> out0(max_states, 0), out1(max_states, 0), state0(max_states, 0), state1(max_states, 0), tail(max_states, 0);
   if (codeType)
   {
      nsc_transit(out0.data(), state0.data(), 0, g_encoder.data(), KK, nn);
      nsc_transit(out1.data(), state1.data(), 1, g_encoder.data(), KK, nn);
      if (codeType == 2)
	 tail[0] = -1;
   }
   else
   {
      rsc_transit(out0.data(), state0.data(), 0, g_encoder.data(), KK, nn);
      rsc_transit(out1.data(), state1.data(), 1, g_encoder.data(), KK, nn);
      rsc_tail(tail.data(), g_encoder.data(), max_states, mm);
   }

   conv_encode(encoded_out, bits, out0.data(), state0.data(), out1.data(), state1.data(), tail.data(), KK, DataLength, nn);
}
