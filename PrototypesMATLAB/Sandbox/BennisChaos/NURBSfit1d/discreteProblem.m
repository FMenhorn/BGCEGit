function [ Rji,u ] = discreteProblem( p ,X)
%DISCRETEBASIS Summary of this function goes here
%   Detailed explanation goes here
u=discreteParametrization(X);

global knot_vector;
m=numel(u);
Rji=zeros(m,numel(knot_vector)- p);
for i = 1 : numel(knot_vector)- p
    for j = 1:m
        Rji(j,i) = bspline_basis(i-1,p,knot_vector, u(j));
    end
end
end

