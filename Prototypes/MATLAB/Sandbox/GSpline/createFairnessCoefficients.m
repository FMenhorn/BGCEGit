function [ lin_coefs ] = createFairnessCoefficients(symIntegVar1, symIntegVar2, symDiffVar1, symDiffVar2, degreeNumeric)
%createFairnessCoefficients Summary of this function goes here
%   Detailed explanation goes here

lin_coefs = zeros(degreeNumeric+1,degreeNumeric+1);

bernsPoly = @(u,n,i) nchoosek(n,i)*u.^i .* (1-u).^(n-i);

for i = 0:degreeNumeric
    for j = 0:degreeNumeric
        bernsProduct = bernsPoly(symIntegVar1,degreeNumeric,i) * bernsPoly(symIntegVar2,degreeNumeric,j);
        diffBerns = diff(diff(bernsProduct,symDiffVar1,1),symDiffVar2,1);
        lin_coefs(i+1,j+1) = int(int(diffBerns,symIntegVar1,0,1),symIntegVar2,0,1);
    end
end
end