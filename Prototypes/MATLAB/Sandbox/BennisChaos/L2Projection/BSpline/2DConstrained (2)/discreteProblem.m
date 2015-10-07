function [ Rji,u ] = discreteProblem( n,X,w )
%DISCRETEBASIS Summary of this function goes here
%   Detailed explanation goes here

u=discreteParametrization(X);

M=numel(u);
m=numel(w)-1;

Rji=zeros(M,1+m);

for i = 0:n
    for j = 1:M
        Rji(j,i+1)=rationalBasis(i,n,w,u(j));
    end
end

end

