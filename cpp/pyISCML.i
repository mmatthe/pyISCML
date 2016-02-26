%module pyISCML
%{
   #define SWIG_FILE_WITH_INIT
  extern "C" void ldpcEncode(int* bits, int sizeBits,
			     int* H_rows, int sizeR1, int sizeR2,
			     int* P, int sizeP1, int sizeP2,
			     int* encoded, int sizeEnc);

extern "C" void MpDecode(double* input, int CodeLength,
			 double* H_rows, int max_row_weight, int NumberParityBits,
			 double* H_cols, int max_col_weight, int NumberRowsHcols,
			 int max_iter, int dec_type, float r_scale_factor, float q_scale_factor,
			 int* data_int, int DataLength,
			 double* llrOut, int sizeDB2, int sizeDB1,
			 int* BitErrors, int sizeBE);

extern "C" void ConvEncode(int* bits, int sizeBits,
			   int* g, int sizeG1, int sizeG2,
			   int codeType,
			   int* encoded_out, int sizeOut);

extern "C" void SisoDecode(double* input_u, int size_u,
			   double* input_c, int size_c,
			   int*   g, int sizeG1, int sizeG2,
			   int code_type,
			   int decoder_type,
			   double* output_u, int size_uo,
			   double* output_c, int size_uc);


%}

%include "cpp/numpy.i"

%init %{
   import_array();
%}


%apply (int* IN_ARRAY1, int DIM1) {(int* bits, int sizeBits)}
%apply (int* IN_ARRAY2, int DIM1, int DIM2) {(int* H_rows, int sizeR1, int sizeR2)}
%apply (int* IN_ARRAY2, int DIM1, int DIM2) {(int* P, int sizeP1, int sizeP2)}
%apply (int* INPLACE_ARRAY1, int DIM1) {(int* encoded, int sizeEnc)}
extern "C" void ldpcEncode(int* bits, int sizeBits,
			   int* H_rows, int sizeR1, int sizeR2,
			   int* P, int sizeP1, int sizeP2,
			   int* encoded, int sizeEnc);

%apply (double* IN_ARRAY1, int DIM1) {(double* input, int CodeLength)}
%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(double* H_rows, int max_row_weight, int NumberParityBits)}
%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(double* H_cols, int max_col_weight, int NumberRowsHcols)}
%apply (int* IN_ARRAY1, int DIM1) {(int* data_int, int DataLength)}
%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) {(double* llrOut, int sizeDB2, int sizeDB1)}
%apply (int* INPLACE_ARRAY1, int DIM1) {(int* BitErrors, int sizeBE)}
extern "C" void MpDecode(double* input, int CodeLength,
			 double* H_rows, int max_row_weight, int NumberParityBits,
			 double* H_cols, int max_col_weight, int NumberRowsHcols,
			 int max_iter, int dec_type, float r_scale_factor, float q_scale_factor,
			 int* data_int, int DataLength,
			 double* llrOut, int sizeDB2, int sizeDB1,
			 int* BitErrors, int sizeBE);

%apply (int* IN_ARRAY1, int DIM1) {(int* bits, int sizeBits)}
%apply (int* IN_ARRAY2, int DIM1, int DIM2) {(int* g, int sizeG1, int sizeG2)}
%apply (int* ARGOUT_ARRAY1, int DIM1) {(int* encoded_out, int sizeOut)};
extern "C" void ConvEncode(int* bits, int sizeBits,
			   int* g, int sizeG1, int sizeG2,
			   int codeType,
			   int* encoded_out, int sizeOut);


%apply (double* IN_ARRAY1, int DIM1) {(double* input_u, int size_u)}
%apply (double* IN_ARRAY1, int DIM1) {(double* input_c, int size_c)}
%apply (int* IN_ARRAY2, int DIM1, int DIM2) {(int* g, int sizeG1, int sizeG2)}
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* output_u, int size_uo)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* output_c, int size_co)};
extern "C" void SisoDecode(double* input_u, int size_u,
			   double* input_c, int size_c,
			   int*   g, int sizeG1, int sizeG2,
			   int code_type,
			   int decoder_type,
			   double* output_u, int size_uo,
			   double* output_c, int size_co);
