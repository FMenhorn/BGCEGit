%% script for testing that the coefs from function are same as coefs used in scheme(and getBicubicPatchIndex)

% utility for shifting indices cyclically in an array
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);

% run to get an actual smooth bicubic bezier patch.
extraOrdCorner;

% The last values stored in As, Bs and Cs are the ones from the last patch,
% thus should access indices shifted cyclically to the last one.

% list of indices [m, 1, 2, ..., m-1]
indShift = shifted_indices(m,m);

% The testing patch to be created through using the coefficients
patch_test = zeros(3,4,4);
[Acoef,B1coefs,B2coefs,Ccoefs] = createBicubicCoefMatrices(m);

% Create each bezier point (i,j) by multiplying the point coordinates with
% the respective coefficient.
for j = 1:4
    for i = 1:4
        for p = 1:m
            patch_test(:,i,j) = patch_test(:,i,j) + ...
                Acoef(p,i,j) * As(:,indShift(p)) + ...
                B1coefs(p,i,j) * Bs(:,1,indShift(p)) + ...
                B2coefs(p,i,j) * Bs(:,2,indShift(p)) + ...
                Ccoefs(p,i,j) * Cs(:,indShift(p));
        end
    end
end

% Output difference of coefficient-generated bezier control points to the
% one from the original peter's scheme (last patch). Should be zero.
patch - patch_test