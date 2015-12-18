function [ summy ] = createFairnessCoefficientsSquares(symIntegVar1, symIntegVar2, symDiffVar1, symDiffVar2, degreeNumeric)
%createFairnessCoefficients Summary of this function goes here
%   Detailed explanation goes here

% lin_coefs = zeros(degreeNumeric+1,degreeNumeric+1);

bernsPoly = @(u,n,i) nchoosek(n,i)*u.^i .* (1-u).^(n-i);

BezPoints = sym('Bpoints',[degreeNumeric+1 degreeNumeric+1]);
BezProducts = sym('Bprods',[degreeNumeric+1 degreeNumeric+1]);
BezPoints = sym('Bpoints',[degreeNumeric+1 degreeNumeric+1]);

for i = 0:degreeNumeric
    for j = 0:degreeNumeric
        bernsProduct = bernsPoly(symIntegVar1,degreeNumeric,i) * bernsPoly(symIntegVar2,degreeNumeric,j);
        diffBerns = diff(diff(bernsProduct,symDiffVar1,1),symDiffVar2,1);
        BezProducts(i+1,j+1) = diffBerns * BezPoints(i+1,j+1);
    end
end


summy = int(int(sum(sum(BezProducts))^2,symIntegVar1,0,1),symIntegVar2,0,1);

end