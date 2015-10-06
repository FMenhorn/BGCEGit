function [ u ] = discreteParametrization( X )
%DISCRETEPARAMETRIZATION Summary of this function goes here
%   Detailed explanation goes here

e = 1;
n = size(X,1);
u = zeros(n,1);
u(1)=0;

nominator = 0;
denominator = 0;

for j = 1:n-1
    denominator = denominator + (norm(X(j+1,:)-X(j,:)))^e;
end

for i = 2:n
    j=i-1;
    nominator = nominator + (norm(X(j+1,:)-X(j,:)))^e;
    
    nextU=nominator/denominator;
    u(i)=nextU;
end

end

