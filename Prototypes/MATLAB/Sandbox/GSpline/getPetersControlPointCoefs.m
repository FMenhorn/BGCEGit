function coefsMatrix = getPetersControlPointCoefs(bezierCoefs, coefs_raw)
% Spits out an nxm matrix of the coefficients on the neighbouring (and 
% central) vertex points to that in the center of the patch, for the bezier
% points specified in the input and the bezier-to-control-point
% coefficients in coefs_raw.

m = size(coefs_raw, 2);
n = size(coefs_raw, 1);
coefsMatrix = zeros(n,m);

for j = 1:n
    for i = 1:n

        controlPointCoef = bezierCoefs(i,j);
        for l = 1:m
            for k = 1:n
                coefsMatrix(k,l) = coefsMatrix(k,l) + coefs_raw(k,l,i,j) * controlPointCoef;
            end
        end
    end
end





end
