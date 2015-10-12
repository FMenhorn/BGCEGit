%% script for testing that the coefs from function are same as coefs used in scheme(and getBicubicPatchIndex)

extraOrdCorner;

patch_test = zeros(3,4,4);
[Acoef,B1coefs,B2coefs,Ccoefs] = createBicubicCoefMatrices(m);

shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
indShift = shifted_indices(m,m);

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
patch - patch_test