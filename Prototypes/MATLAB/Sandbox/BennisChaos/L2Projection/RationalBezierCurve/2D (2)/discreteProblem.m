function [ Rji,u ] = discreteProblem( n,X,w )
%DISCRETEBASIS Summary of this function goes here
%   Detailed explanation goes here

u=discreteParametrization(X);

m=numel(u);

Rji=zeros(m,1+n);

for i = 0:n
    for j = 1:m
        Rji(j,i+1)=rationalBasis(i,w,u(j));
    end
end

end

