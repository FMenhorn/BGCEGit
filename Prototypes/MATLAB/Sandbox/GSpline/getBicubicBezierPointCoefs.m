function coefsMatrix = getBicubicBezierPointCoefs(localParams, coefs_raw)
% Spits out an mx4 matrix of the coefficients on the neighbouring (and 
% central) vertex points to that in the center of the patch, for a point 
% with the local parameters localParams on the patch. The first column is
% the A coef, the second the B1 coefs, the third the B2 coefs, and the
% fourth the C coefs.

m = size(coefs_raw, 2);
coefsMatrix = zeros(4,m);

for j = 1:4
    for i = 1:4
        % -1 since matlab uses indices from 1-4 instead of 0-3 and the
        % bernstein degree is ^3
        controlPointCoef = bernstein(i-1,3,localParams(1)) * bernstein(j-1,3,localParams(2));
        for l = 1:m
            for k = 1:4
                coefsMatrix(k,l) = coefsMatrix(k,l) + coefs_raw(k,l,i,j) * controlPointCoef;
            end
        end
    end
end





end
