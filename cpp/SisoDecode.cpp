#include <iostream>
#include <vector>
#include <stdexcept>

#include <math.h>

#include "cmlIncludes/convolutional.h"
#include "cmlIncludes/maxstar.h"
#include "cmlIncludes/siso.h"

extern "C" void SisoDecode(double* input_u, int size_u,
			   double* input_c, int size_c,
			   int*   g, int sizeG1, int sizeG2,
			   int codeType,
			   int decoder_type,
			   double* output_u, int size_uo,
			   double* output_c, int size_co)
{
   int nn = sizeG1;
   int KK = sizeG2;
   int mm = KK -1;
   int max_states = 1 << mm;

   int DataLength = size_u;
   int CodeLength = size_c;
   if ( CodeLength != nn*(DataLength+mm) )
      throw std::runtime_error("Data length and Code length do not match!");


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

   std::vector<float> input_u_float(input_u, input_u + DataLength);
   std::vector<float> input_c_float(input_c, input_c + CodeLength);
   std::vector<int> out0(max_states, 0), out1(max_states, 0), state0(max_states, 0), state1(max_states, 0);
   if (codeType)
   {
      nsc_transit(out0.data(), state0.data(), 0, g_encoder.data(), KK, nn);
      nsc_transit(out1.data(), state1.data(), 1, g_encoder.data(), KK, nn);
   }
   else
   {
      rsc_transit(out0.data(), state0.data(), 0, g_encoder.data(), KK, nn);
      rsc_transit(out1.data(), state1.data(), 1, g_encoder.data(), KK, nn);
   }

   std::vector<float> output_c_float(CodeLength, 0);
   std::vector<float> output_u_float(DataLength, 0);
   siso(output_u_float.data(), output_c_float.data(), out0.data(), state0.data(), out1.data(), state1.data(), input_u_float.data(), input_c_float.data(), KK, nn, DataLength, decoder_type);

   std::copy(output_u_float.begin(), output_u_float.end(), output_u);
   std::copy(output_c_float.begin(), output_c_float.end(), output_c);
}
