function [ C ] = setupLSQmatrix( x,t,n )
%SETUPLSQMATRIX Summary of this function goes here
%   Detailed explanation goes here

%x is the parameter vector
%t is the knot vector
%n the degree of the spline

C=zeros(numel(x),numel(t)- n);
for i = 1 : numel(t)- n
    for j = 1:numel(x)
        C(j,i) = bspline_basis(i-1,n,t, x(j));
    end
end
end

