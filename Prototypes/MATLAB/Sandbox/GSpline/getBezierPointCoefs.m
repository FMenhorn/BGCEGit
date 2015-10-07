function coefsMatrix = getBezierPointCoefs(localParams)
% Spits out a 3x3 matrix of the coefficients on the neighbouring (and 
% central) vertex points to that in the center of the patch, for a point 
% with the local parameters localParams on the patch.

coefsMatrix = zeros(3);

for i = 1:3
    for j = 1:3
        % -1 since matlab uses indices from 1-3 instead of 0-2 and the
        % bernstein degree is ^2
        controlPointCoef = bernstein(i-1,2,localParams(1)) * bernstein(j-1,2,localParams(2));
        vertexCoefs = getBiquadraticPatchCoefs(i,j);
        coefsMatrix = coefsMatrix + vertexCoefs * controlPointCoef;        
    end
end





end
