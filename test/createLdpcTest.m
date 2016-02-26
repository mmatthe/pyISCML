function createLdpcTest()

%characterizeMpDecode();

createMpDecode()

%createLdpcEncode();
% readLdpcEncode('ldpc56_2304.mat');
%readMpDecode('MpDecode_56_2304.mat');
end

function characterizeMpDecode()

mex -g MpDecode.cpp

bits = double(randn(1, 1920) > 0);
[H_rows, H_cols, P] = InitializeWiMaxLDPC(5/6, 2304, 0);
enc = LdpcEncode(bits, H_rows, P);

sigma2 = 0.3;
noise = sqrt(sigma2)* randn(size(enc));
rx = (2*enc-1) + noise;
llr = -2*rx / (sigma2);

[dec, errors] = MpDecode_orig(llr, H_rows, H_cols, 100, 0, 1, 1, bits);
[dec2, errors2] =    MpDecode(llr, H_rows, H_cols, 100, 0, 1, 1, bits);

assert(sum(abs(dec(:)-dec2(:))) < 1e-6);
assert(sum(abs(errors(:)-errors2(:))) < 1e-6);
end


function createMpDecode()
    function write(fn, rate, ln, sigma2)
        rng(0);
        bits = double(randn(1, rate * ln) > 0);
        [H_rows, H_cols, P] = InitializeWiMaxLDPC(rate, ln, 0);
        enc = LdpcEncode(bits, H_rows, P);
        
        noise = sqrt(sigma2)* randn(size(enc));
        rx = (2*enc-1) + noise;
        llr = -2*rx / (sigma2);
        
        [dec, errors] = MpDecode(llr, H_rows, H_cols, 100, 0, 1, 1, bits);
        save(fn, 'llr', 'dec', 'errors', 'bits', 'H_rows', 'H_cols');
    end

    rates = [1/2, 3/4, 5/6];  rateStr = {'12', '34', '56'};
    noises = [0.65, 0.35, 0.3];
    lengths = [576:96:2304];
    
    for ir=1:length(rates)
        for il=1:length(lengths)
            fn = sprintf('data/MpDecode_%s_%d.mat', rateStr{ir}, lengths(il));
            write(fn, rates(ir), lengths(il), noises(ir));
        end
    end
    
end

function readMpDecode(fn)
load(fn);
[dec, errors] = MpDecode(llr, H_rows, H_cols, 100, 0, 1, 1, bits);
end

function createLdpcEncode()
[H_rows, H_cols, P] = InitializeWiMaxLDPC(5/6, 2304, 0);
bits = double(randn(1,2304*5/6) > 0);
encoded = LdpcEncode(bits, H_rows, P);

save('ldpc56_2304.mat', 'bits', 'encoded');
end

function readLdpcEncode(fn)
    load(fn);
    
    [H_rows, H_cols, P] = InitializeWiMaxLDPC(5/6, 2304, 0);
    enc2 = LdpcEncode(bits, H_rows, P);
end