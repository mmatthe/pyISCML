function createConvolutionalTest()
    %createConvEncode();
    createSisoDecode();
end

function createConvEncode()
    function saveIt(nr, bits, g, code_type)
        encoded = ConvEncode(bits, g, code_type);
        save(sprintf('data/ConvEncode_%d.mat', nr), 'bits', 'g', 'encoded', 'code_type');
    end

    i = 1;
    saveIt(i, [1 0 0 1 0 0 1 0 1 0 1], [1 0 1; 1 1 0], 0);  i = i+1;
    saveIt(i, [1 1 1 1 0 1 0], [1 0 0; 1 1 1; 1 0 1], 0);   i = i+1;
    saveIt(i, double(randn(1, 10000) > 0), [1 1 1 0 1 0 1 1; 1 0 0 1 0 0 1 1], 0);  i = i+1;

    saveIt(i, [1 0 0 1 0 0 1 0 1 0 1], [1 0 1; 1 1 0], 1);  i = i+1;
    saveIt(i, [1 1 1 1 0 1 0], [1 0 0; 1 1 1; 1 0 1], 1);   i = i+1;
    saveIt(i, double(randn(1, 10000) > 0), [1 1 1 0 1 0 1 1; 1 0 0 1 0 0 1 1], 1);  i = i+1;

    saveIt(i, [1 0 0 1 0 0 1 0 1 0 1], [1 0 1; 1 1 0], 2);  i = i+1;
    saveIt(i, [1 1 1 1 0 1 0], [1 0 0; 1 1 1; 1 0 1], 2);   i = i+1;
    saveIt(i, double(randn(1, 10000) > 0), [1 1 1 0 1 0 1 1; 1 0 0 1 0 0 1 1], 2);  i = i+1;
    
end

function createSisoDecode()
    function saveIt(nr, bits, g, code_type, sigma, decoder_type)
        encoded = ConvEncode(bits, g, code_type);    
        input_u = zeros(size(bits));
        input_c = 1 - 2*encoded + sigma * randn(size(encoded));
    
        [decoded_u, decoded_c] = SisoDecode(input_u, input_c, g, code_type, decoder_type);
        dec_us = double(decoded_u < 0);
        save(sprintf('data/SisoDecode_%d.mat', nr), 'bits', 'g', 'code_type', 'sigma', 'input_c', 'decoder_type', 'decoded_u', 'decoded_c');
    end
    rand('seed', 0);
    randn('seed', 0);
    
    bits = [1 0 1 0 0 1 0 1 1 0 1 1 0];
    g = [1 0 1; 1 1 0;];    
    i=1;
    for code_type = [0, 1]
        for decoder_type = [0, 1, 2, 3, 4]
            for sigma = [0.1, 1, 2]
                bits = double(randn(1, 100) < 0);
                g = double(randn(randi(3)+1, randi(7)+1) > 0);
                saveIt(i, bits, g, code_type, sigma, decoder_type);                
                i = i+1;
            end
        end
    end

end